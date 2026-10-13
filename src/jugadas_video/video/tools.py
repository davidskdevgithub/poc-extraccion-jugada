"""Invocación de herramientas externas (ffmpeg, ffprobe).

Punto único para comprobar disponibilidad y ejecutar comandos externos
con errores visibles (architecture.md §3.J).
"""

import shutil
import subprocess


class ExternalToolMissingError(RuntimeError):
    """Una herramienta externa requerida no está disponible."""


class VideoToolError(RuntimeError):
    """Una herramienta externa falló al procesar una entrada."""


def require_tool(name: str) -> str:
    """Devuelve la ruta del ejecutable o lanza ExternalToolMissingError."""
    found = shutil.which(name)
    if found is None:
        msg = (
            f"la herramienta externa '{name}' no está disponible en el "
            "PATH; instálala (Homebrew) y autorízala antes de reintentar"
        )
        raise ExternalToolMissingError(msg)
    return found


def run_tool(
    args: list[str], timeout: float = 120.0
) -> subprocess.CompletedProcess:
    """Ejecuta una herramienta externa y valida que termine con éxito.

    Lanza ExternalToolMissingError si el ejecutable no existe y
    VideoToolError si el comando falla, incluyendo el inicio de stderr.
    """
    require_tool(args[0])
    try:
        proc = subprocess.run(
            args, capture_output=True, text=True, check=False, timeout=timeout
        )
    except subprocess.TimeoutExpired as exc:
        msg = f"el comando excedió el tiempo límite ({timeout}s): {args[0]}"
        raise VideoToolError(msg) from exc
    if proc.returncode != 0:
        stderr = (proc.stderr or "").strip()
        msg = (
            f"el comando '{args[0]}' falló con código {proc.returncode}: "
            f"{stderr[:500]}"
        )
        raise VideoToolError(msg)
    return proc
