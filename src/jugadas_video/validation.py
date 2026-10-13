"""Validaciones de la etapa E0 (UC-E7 y UC-E2)."""

import math
from pathlib import Path


class ValidationError(Exception):
    """Error base para las validaciones de entrada."""


class InvalidIntervalError(ValidationError):
    """El intervalo solicitado de análisis no es válido."""


class InvalidVideoFileError(ValidationError):
    """El archivo de video de entrada no es válido."""


def validate_interval(
    start: float,
    end: float,
    known_duration: float | None = None,
) -> tuple[float, float]:
    """Valida el intervalo solicitado de análisis.

    Rechaza valores no finitos, start negativo, end <= start y, si se
    conoce la duración del video, end que la exceda. No recorta
    silenciosamente nada; devuelve (start, end) como floats.
    """
    if not math.isfinite(start):
        msg = f"start no es finito: {start!r}"
        raise InvalidIntervalError(msg)
    if not math.isfinite(end):
        msg = f"end no es finito: {end!r}"
        raise InvalidIntervalError(msg)
    if start < 0:
        msg = f"start no puede ser negativo: {start}"
        raise InvalidIntervalError(msg)
    if end <= start:
        msg = f"end ({end}) debe ser mayor que start ({start})"
        raise InvalidIntervalError(msg)
    if known_duration is not None and end > known_duration:
        excess = end - known_duration
        msg = (
            f"end ({end}) excede la duración conocida del video "
            f"({known_duration}) por {excess} s"
        )
        raise InvalidIntervalError(msg)
    return (float(start), float(end))


def validate_video_file(path: Path) -> Path:
    """Valida un archivo de video de entrada.

    Rechaza rutas inexistentes, directorios, archivos vacíos y archivos
    sin la firma de contenedor MP4/ISO-BMFF ('ftyp' en el offset 4).
    Devuelve la ruta resuelta.
    """
    resolved = path.resolve()
    if not resolved.exists():
        msg = f"el archivo no existe: {resolved}"
        raise InvalidVideoFileError(msg)
    if not resolved.is_file():
        msg = f"la ruta no es un archivo regular: {resolved}"
        raise InvalidVideoFileError(msg)
    if resolved.stat().st_size == 0:
        msg = f"el archivo está vacío: {resolved}"
        raise InvalidVideoFileError(msg)
    with resolved.open("rb") as fh:
        header = fh.read(12)
    if len(header) < 12 or header[4:8] != b"ftyp":
        msg = (
            f"el archivo no tiene la firma de contenedor "
            f"MP4/ISO-BMFF ('ftyp'): {resolved}"
        )
        raise InvalidVideoFileError(msg)
    return resolved
