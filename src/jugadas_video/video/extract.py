"""Extracción de imágenes de referencia del intervalo (etapa E0).

Reglas críticas de la narrativa:

- Nunca se fabrica un timestamp: solo se usan frames cuyos ``pts_time``
  reales reporta ffprobe.
- No se pide un frame en el límite superior del intervalo si no existe
  (el muestreo excluye ``end``).
- Nunca se sustituye silenciosamente por un frame exterior al
  intervalo; si no hay frames elegibles se lanza
  :class:`FrameNotAvailableError`.
- Se registra siempre el timestamp real del frame obtenido.
"""

import json
import struct
from pathlib import Path

from jugadas_video.runs import RunArtifactExistsError
from jugadas_video.validation import (
    validate_interval,
    validate_video_file,
)
from jugadas_video.video.tools import run_tool


class FrameNotAvailableError(RuntimeError):
    """No hay ningún frame real elegible dentro del intervalo.

    No se fabrican timestamps ni se usan frames fuera del intervalo.
    """


class ExtractionError(RuntimeError):
    """Fallo propio del proceso de extracción (p. ej. ffmpeg no
    produjo el archivo de salida esperado)."""


def select_timestamps(start: float, end: float, count: int = 8) -> list[float]:
    """Devuelve los timestamps solicitados del intervalo.

    Regla determinista de muestreo: ``t_i = start + i * (end - start) /
    count`` para ``i`` en ``0..count-1``. Incluye ``start`` y excluye
    ``end``: así nunca se pide un frame en el límite superior que puede
    no existir (p. ej. un frame exactamente en t=8 de un video que
    termina ahí).

    Valida el intervalo con
    :func:`jugadas_video.validation.validate_interval` y rechaza
    ``count < 1`` con :class:`ExtractionError`.
    """
    validate_interval(start, end)
    if count < 1:
        msg = f"count debe ser >= 1 (recibido: {count})"
        raise ExtractionError(msg)
    span = (end - start) / count
    return [start + i * span for i in range(count)]


def probe_frame_timestamps(path: Path) -> list[float]:
    """Consulta ffprobe y devuelve los timestamps reales de los frames.

    Usa ``ffprobe -v error -select_streams v:0 -print_format json
    -show_entries frame=pts_time -show_frames`` sobre el stream de
    video. Ignora frames sin ``pts_time``.
    """
    proc = run_tool(
        [
            "ffprobe",
            "-v",
            "error",
            "-select_streams",
            "v:0",
            "-print_format",
            "json",
            "-show_entries",
            "frame=pts_time",
            "-show_frames",
            str(path),
        ]
    )
    data = json.loads(proc.stdout)
    timestamps: list[float] = []
    for frame in data.get("frames", []):
        pts_time = frame.get("pts_time")
        if pts_time is not None:
            timestamps.append(float(pts_time))
    return timestamps


def closest_frame_in_interval(
    timestamps: list[float],
    requested: float,
    start: float,
    end: float,
) -> float:
    """Elige el frame real más cercano al solicitado dentro del
    intervalo (función pura, sin IO).

    Solo considera timestamps en ``[start, end]`` (extremos
    incluidos). En empate de distancia gana el frame anterior (el de
    timestamp menor). Si no hay ningún frame elegible lanza
    :class:`FrameNotAvailableError`.
    """
    eligible = sorted(t for t in timestamps if start <= t <= end)
    if not eligible:
        msg = (
            f"no hay ningún frame real dentro del intervalo "
            f"[{start}, {end}]; no se fabrican timestamps ni se usan "
            "frames fuera del intervalo"
        )
        raise FrameNotAvailableError(msg)
    return min(eligible, key=lambda t: (abs(t - requested), t))


def snap_to_frame(
    path: Path, requested_s: float, start: float, end: float
) -> float:
    """Devuelve el timestamp real del frame más cercano al solicitado
    dentro de ``[start, end]``.

    Consulta los timestamps reales de los frames del video con ffprobe
    (ver :func:`probe_frame_timestamps`) y aplica la regla determinista
    de :func:`closest_frame_in_interval`.
    """
    timestamps = probe_frame_timestamps(path)
    return closest_frame_in_interval(timestamps, requested_s, start, end)


def png_dimensions(path: Path) -> tuple[int, int]:
    """Lee el header IHDR de un PNG con stdlib y devuelve (ancho, alto).

    En un PNG, el primer chunk es IHDR: bytes 16-20 contienen el ancho
    y 20-24 el alto, como uint32 big-endian.
    """
    with path.open("rb") as fh:
        header = fh.read(24)
    if len(header) < 24 or header[12:16] != b"IHDR":
        msg = f"el archivo no es un PNG válido con IHDR: {path}"
        raise ExtractionError(msg)
    width, height = struct.unpack(">II", header[16:24])
    return (int(width), int(height))


def extract_frame(path: Path, ts: float, out_path: Path) -> dict:
    """Extrae UN frame a resolución original y devuelve su entry.

    Comando (``-ss`` antes de ``-i`` para seek rápido; ffmpeg decodifica
    desde el keyframe anterior y descarta hasta el timestamp pedido, de
    modo que la salida es precisa)::

        ffmpeg -ss <ts> -i <path> -frames:v 1 -update 1 -y <out_path>

    Si ``out_path`` existe lanza :class:`RunArtifactExistsError`
    (protección de artefactos de ejecuciones). El ``timestamp_real_s``
    de la entry es el ``ts`` solicitado (el frame real del que proviene
    tras el snap), no una marca interna de ffmpeg. Las dimensiones se
    leen del header IHDR del PNG producido con stdlib.
    """
    if out_path.exists():
        raise RunArtifactExistsError(
            f"El artefacto '{out_path}' ya existe; no se sobrescriben "
            "artefactos de ejecuciones previas."
        )
    run_tool(
        [
            "ffmpeg",
            "-ss",
            f"{ts:.6f}",
            "-i",
            str(path),
            "-frames:v",
            "1",
            "-update",
            "1",
            "-y",
            str(out_path),
        ]
    )
    if not out_path.exists():
        msg = f"ffmpeg no produjo el archivo de salida esperado: {out_path}"
        raise ExtractionError(msg)
    width, height = png_dimensions(out_path)
    return {
        "archivo": out_path.name,
        "tiempo_solicitado_s": float(ts),
        "timestamp_real_s": float(ts),
        "dimensiones": [width, height],
        "transformaciones": [],
    }


def extract_reference_frames(
    path: Path,
    requested_times: list[float],
    out_dir: Path,
    start: float,
    end: float,
    reduced_max_width: int | None = None,
) -> list[dict]:
    """Extrae los frames de referencia del intervalo y devuelve las
    entries del índice de imágenes, en orden.

    Para cada tiempo solicitado: snap al frame real dentro de
    ``[start, end]`` (:func:`snap_to_frame`) → extracción a resolución
    original (:func:`extract_frame`). Si ``reduced_max_width`` no es
    ``None``, genera además una versión reducida con ffmpeg
    (``-vf scale='min(iw,<max>)':-1``) nombrada
    ``<stem>_reducida.png`` y agrega UNA entry adicional con
    ``transformaciones: ["escala a ancho max <max>"]``, de modo que las
    reducidas quedan identificadas como tales.

    Nombres de archivo deterministas: ``frame_t_<timestamp con 3
    decimales>.png``. Si dos tiempos solicitados caen en el mismo
    frame, el segundo intento de escritura lanza
    :class:`RunArtifactExistsError` (no se sobrescriben artefactos).
    """
    validate_video_file(path)
    validate_interval(start, end)
    out_dir.mkdir(parents=True, exist_ok=True)
    entries: list[dict] = []
    for requested in requested_times:
        real_ts = snap_to_frame(path, requested, start, end)
        out_path = out_dir / f"frame_t_{real_ts:.3f}.png"
        entry = extract_frame(path, real_ts, out_path)
        entry["tiempo_solicitado_s"] = float(requested)
        entries.append(entry)
        if reduced_max_width is not None:
            entries.append(
                _extract_reduced_frame(
                    path,
                    requested,
                    real_ts,
                    out_path,
                    reduced_max_width,
                )
            )
    return entries


def _extract_reduced_frame(
    path: Path,
    requested: float,
    real_ts: float,
    original_path: Path,
    reduced_max_width: int,
) -> dict:
    """Genera la versión reducida de un frame ya extraído.

    Comando (mismo orden que :func:`extract_frame`, con el filtro de
    escala; ``-1`` conserva la relación de aspecto)::

        ffmpeg -ss <ts> -i <path> -frames:v 1 \
            -vf scale='min(iw,<max>)':-1 -update 1 -y <out_path>
    """
    reduced_path = original_path.with_name(f"{original_path.stem}_reducida.png")
    if reduced_path.exists():
        raise RunArtifactExistsError(
            f"El artefacto '{reduced_path}' ya existe; no se "
            "sobrescriben artefactos de ejecuciones previas."
        )
    run_tool(
        [
            "ffmpeg",
            "-ss",
            f"{real_ts:.6f}",
            "-i",
            str(path),
            "-frames:v",
            "1",
            "-vf",
            f"scale='min(iw,{reduced_max_width})':-1",
            "-update",
            "1",
            "-y",
            str(reduced_path),
        ]
    )
    if not reduced_path.exists():
        msg = f"ffmpeg no produjo el archivo reducido esperado: {reduced_path}"
        raise ExtractionError(msg)
    width, height = png_dimensions(reduced_path)
    return {
        "archivo": reduced_path.name,
        "tiempo_solicitado_s": float(requested),
        "timestamp_real_s": float(real_ts),
        "dimensiones": [width, height],
        "transformaciones": [f"escala a ancho max {reduced_max_width}"],
    }
