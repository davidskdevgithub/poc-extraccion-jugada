"""Inspección de video con ffprobe (UC-02, etapa E0).

Lee metadatos del contenedor y del primer stream de video, y los
timestamps por frame de un intervalo. No infiere uniformidad temporal
desde el FPS nominal: lo que no puede determinarse se declara de forma
explícita en la lista `indeterminados` (UC-E4).
"""

import json
import math
from pathlib import Path

from jugadas_video.validation import validate_interval, validate_video_file
from jugadas_video.video.tools import run_tool

# Tolerancia relativa para decidir si los gaps entre timestamps son
# constantes (decisión documentada: 1e-6 respecto del intervalo de
# referencia; ver _compute_temporal_metrics).
TOLERANCIA_RELATIVA_FPS = 1e-6


class InspectionError(RuntimeError):
    """Fallo de interpretación propia del módulo de inspección."""


def ffprobe_json(path: Path) -> tuple[dict, str]:
    """Ejecuta ffprobe sobre `path` y devuelve (json, texto crudo).

    El texto crudo se devuelve para que el llamador pueda conservar la
    salida original de ffprobe. Lanza InspectionError si la salida no
    es un objeto JSON válido.
    """
    proc = run_tool(
        [
            "ffprobe",
            "-v",
            "error",
            "-print_format",
            "json",
            "-show_format",
            "-show_streams",
            str(path),
        ]
    )
    raw = proc.stdout
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        msg = f"ffprobe no devolvió JSON válido para {path}: {exc}"
        raise InspectionError(msg) from exc
    if not isinstance(data, dict):
        msg = f"la salida de ffprobe para {path} no es un objeto JSON"
        raise InspectionError(msg)
    return data, raw


def _first_video_stream(data: dict) -> dict:
    """Devuelve el primer stream con codec_type 'video' (UC-E2)."""
    streams = data.get("streams")
    if not isinstance(streams, list):
        msg = (
            "ffprobe no reporta 'streams' como lista para el archivo; "
            "no se puede interpretar la entrada (UC-E2)"
        )
        raise InspectionError(msg)
    for stream in streams:
        if isinstance(stream, dict) and stream.get("codec_type") == "video":
            return stream
    msg = (
        "ffprobe no reporta ningún stream de video en el archivo: la "
        "entrada no es un video utilizable (UC-E2)"
    )
    raise InspectionError(msg)


def _as_int(value: object) -> int | None:
    """Convierte a int o devuelve None si no es parseable."""
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        try:
            return int(value)
        except ValueError:
            return None
    return None


def _as_float(value: object) -> float | None:
    """Convierte a float finito o devuelve None si no es parseable."""
    if isinstance(value, bool):
        return None
    if isinstance(value, int | float):
        parsed = float(value)
        return parsed if math.isfinite(parsed) else None
    if isinstance(value, str):
        try:
            parsed = float(value)
        except ValueError:
            return None
        return parsed if math.isfinite(parsed) else None
    return None


def _parse_frame_rate(value: object) -> float | None:
    """Parsea una fracción 'N/D' de ffprobe o devuelve None.

    Trata como indeterminadas: None, cadenas vacías, 'N/A', '0/0',
    denominador cero y tasas no positivas o no finitas.
    """
    if not isinstance(value, str) or not value.strip():
        return None
    text = value.strip()
    parts = text.split("/")
    try:
        if len(parts) == 2:
            numerator = float(parts[0])
            denominator = float(parts[1])
        else:
            numerator = float(text)
            denominator = 1.0
    except ValueError:
        return None
    if denominator == 0 or numerator <= 0:
        return None
    rate = numerator / denominator
    if not math.isfinite(rate) or rate <= 0:
        return None
    return rate


def _rotation_degrees(stream: dict) -> float | None:
    """Grados de rotación declarados para el stream, o None.

    Busca primero el tag 'rotate' y luego el side data 'Display
    Matrix' (displaymatrix). El valor se devuelve tal como lo expone
    ffprobe, sin normalizar signo ni convención.
    """
    tags = stream.get("tags")
    if isinstance(tags, dict):
        rotate = _as_float(tags.get("rotate"))
        if rotate is not None:
            return rotate
    side_data_list = stream.get("side_data_list")
    if isinstance(side_data_list, list):
        for side_data in side_data_list:
            if not isinstance(side_data, dict):
                continue
            side_type = str(side_data.get("side_data_type", "")).lower()
            if "displaymatrix" not in side_type.replace(" ", ""):
                continue
            for key, val in side_data.items():
                if "rotation" in key:
                    rotation = _as_float(val)
                    if rotation is not None:
                        return rotation
    return None


def _reported_duration(
    data: dict, stream: dict, indeterminados: list[str]
) -> float | None:
    """Duración reportada: prefiere format.duration, luego stream."""
    fmt = data.get("format")
    duration = None
    if isinstance(fmt, dict):
        duration = _as_float(fmt.get("duration"))
    if duration is None:
        duration = _as_float(stream.get("duration"))
    if duration is None:
        indeterminados.append(
            "duracion_reportada_s: ni 'format.duration' ni "
            "'stream.duration' están presentes o son parseables"
        )
    return duration


def inspect_file(path: Path) -> dict:
    """Inspecciona el archivo y devuelve un resumen legible (UC-02).

    Valida el archivo antes de invocar ffprobe (UC-E2) y falla con
    InspectionError si no hay streams de video. Todo lo que no pueda
    determinarse se declara en 'indeterminados' con su motivo (UC-E4).
    """
    resolved = validate_video_file(path)
    data, _raw = ffprobe_json(resolved)
    stream = _first_video_stream(data)
    indeterminados: list[str] = []

    duration = _reported_duration(data, stream, indeterminados)

    codec = stream.get("codec_name")
    if not isinstance(codec, str) or not codec:
        codec = None
        indeterminados.append(
            "codec: el stream de video no declara 'codec_name'"
        )

    width = _as_int(stream.get("width"))
    if width is None:
        indeterminados.append(
            "ancho: el stream de video no declara 'width' parseable"
        )
    height = _as_int(stream.get("height"))
    if height is None:
        indeterminados.append(
            "alto: el stream de video no declara 'height' parseable"
        )

    raw_fps = stream.get("avg_frame_rate")
    fps_nominal = _parse_frame_rate(raw_fps)
    if fps_nominal is None:
        indeterminados.append(
            "fps_nominal: 'avg_frame_rate' "
            f"({raw_fps!r}) no es una fracción utilizable; no implica "
            "FPS variable ni uniforme (UC-E4)"
        )

    time_base = stream.get("time_base")
    if not isinstance(time_base, str) or not time_base:
        time_base = None
        indeterminados.append(
            "time_base: el stream de video no declara 'time_base'"
        )

    return {
        "duracion_reportada_s": duration,
        "codec": codec,
        "ancho": width,
        "alto": height,
        "rotacion_grados": _rotation_degrees(stream),
        "fps_nominal": fps_nominal,
        "time_base": time_base,
        "indeterminados": indeterminados,
    }


def _video_frame_timestamps(path: Path) -> tuple[list[float], int]:
    """Timestamps de los frames del primer stream de video.

    Devuelve (timestamps ordenados, cantidad de frames omitidos por no
    tener 'pts_time' parseable).
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
    try:
        data = json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        msg = f"ffprobe no devolvió JSON válido para {path}: {exc}"
        raise InspectionError(msg) from exc
    if not isinstance(data, dict):
        msg = f"la salida de ffprobe para {path} no es un objeto JSON"
        raise InspectionError(msg)
    frames = data.get("frames")
    if not isinstance(frames, list):
        return [], 0
    timestamps: list[float] = []
    skipped = 0
    for frame in frames:
        pts_time = frame.get("pts_time") if isinstance(frame, dict) else None
        parsed = _as_float(pts_time)
        if parsed is None:
            skipped += 1
            continue
        timestamps.append(parsed)
    return sorted(timestamps), skipped


def frame_timestamps(path: Path, start: float, end: float) -> list[float]:
    """Timestamps de los frames de video dentro de [start, end].

    Valida el intervalo sin known_duration: el llamador decide si se
    la pasa. Los frames sin 'pts_time' parseable se omiten aquí y se
    registran en temporal_summary (UC-E4). Si no hay frames en el
    intervalo devuelve una lista vacía: no es un error (UC-E3).
    """
    validate_interval(start, end)
    resolved = validate_video_file(path)
    timestamps, _skipped = _video_frame_timestamps(resolved)
    return [t for t in timestamps if start <= t <= end]


def _compute_temporal_metrics(
    timestamps: list[float], nominal_fps: float | None
) -> tuple[float | None, bool | None, list[str]]:
    """Calcula (fps_efectivo, fps_variable, notas) desde timestamps.

    fps_efectivo es (n_frames - 1) / suma de gaps. fps_variable
    compara cada gap contra un intervalo de referencia con tolerancia
    relativa TOLERANCIA_RELATIVA_FPS: la referencia es 1/fps nominal
    si existe y la media de los gaps si no. Con menos de 2 frames no
    se determina nada (None). No infiere uniformidad desde el FPS
    nominal (UC-E4).
    """
    n = len(timestamps)
    if n < 2:
        return None, None, []
    gaps = [b - a for a, b in zip(timestamps, timestamps[1:])]
    total = sum(gaps)
    fps_efectivo = (n - 1) / total if total > 0 else None
    notes: list[str] = []
    if nominal_fps is not None and nominal_fps > 0:
        reference = 1.0 / nominal_fps
    elif total > 0:
        reference = total / len(gaps)
    else:
        reference = 0.0
    if reference <= 0:
        notes.append(
            "fps_variable: no hay intervalo de referencia utilizable "
            "(fps nominal ausente y gaps nulos)"
        )
        return fps_efectivo, None, notes
    tolerance = TOLERANCIA_RELATIVA_FPS * reference
    fps_variable = any(abs(gap - reference) > tolerance for gap in gaps)
    return fps_efectivo, fps_variable, notes


def temporal_summary(path: Path, start: float, end: float) -> dict:
    """Resume las características temporales del intervalo (UC-02).

    Valida el intervalo y el archivo, lee los timestamps por frame y
    devuelve n_frames, fps efectivo y si los gaps sugieren FPS
    variable. Un intervalo sin frames no es un error: se registra
    explícitamente en 'indeterminados' (UC-E3/UC-E4).
    """
    validate_interval(start, end)
    resolved = validate_video_file(path)
    timestamps, skipped = _video_frame_timestamps(resolved)
    in_range = [t for t in timestamps if start <= t <= end]

    indeterminados: list[str] = []
    if skipped:
        indeterminados.append(
            f"{skipped} frame(s) sin 'pts_time' parseable fueron "
            "omitidos del conteo del intervalo (UC-E4)"
        )

    data, _raw = ffprobe_json(resolved)
    stream = _first_video_stream(data)
    nominal_fps = _parse_frame_rate(stream.get("avg_frame_rate"))
    fps_efectivo, fps_variable, notes = _compute_temporal_metrics(
        in_range, nominal_fps
    )
    indeterminados.extend(notes)

    n_frames = len(in_range)
    if n_frames == 0:
        indeterminados.append(
            f"no hay frames con 'pts_time' dentro de [{start}, {end}]; "
            "no se puede determinar fps efectivo ni variabilidad (no "
            "es un error: es un resultado a registrar)"
        )
    elif n_frames == 1:
        indeterminados.append(
            f"solo hay 1 frame dentro de [{start}, {end}]; se necesita "
            "más de uno para determinar fps efectivo y variabilidad"
        )

    return {
        "intervalo": [start, end],
        "n_frames": n_frames,
        "fps_efectivo": fps_efectivo,
        "fps_variable": fps_variable,
        "primer_frame_s": in_range[0] if in_range else None,
        "ultimo_frame_s": in_range[-1] if in_range else None,
        "indeterminados": indeterminados,
    }
