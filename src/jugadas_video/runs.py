"""Gestión de ejecuciones y artefactos de la etapa E0.

Cada ejecución escribe sus artefactos en ``<base_dir>/<stage>/<run-id>/``.
El run-id se deriva de la marca de tiempo y nunca sobrescribe una
carpeta existente (agrega sufijos ``-2``, ``-3``, ... si hace falta).
"""

import hashlib
import json
from datetime import datetime
from pathlib import Path

IMAGE_INDEX_FILENAME = "indice_imagenes.json"
RUN_RECORD_FILENAME = "registro.json"


class RunArtifactExistsError(RuntimeError):
    """Se intentó sobrescribir un artefacto de una ejecución existente."""


def sha256_file(path: Path) -> str:
    """Devuelve el hash SHA-256 (hex) de un archivo, leyendo por bloques."""
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def create_run_dir(stage: str, base_dir: Path = Path("artifacts")) -> Path:
    """Crea ``base_dir/<stage>/<run-id>/`` y devuelve ese path.

    El run-id tiene formato ``YYYYMMDD-HHMMSS``. Si la carpeta ya
    existe, se prueba con sufijos ``-2``, ``-3``, ... hasta encontrar
    un nombre libre; nunca se sobrescribe una ejecución previa.
    """
    stage_dir = base_dir / stage
    stage_dir.mkdir(parents=True, exist_ok=True)

    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_id = stamp
    counter = 2
    while True:
        run_dir = stage_dir / run_id
        try:
            run_dir.mkdir()
        except FileExistsError:
            run_id = f"{stamp}-{counter}"
            counter += 1
            continue
        return run_dir


def _write_bytes(path: Path, payload: bytes) -> None:
    if path.exists():
        raise RunArtifactExistsError(
            f"El artefacto '{path}' ya existe; no se sobrescriben "
            "artefactos de ejecuciones previas."
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(payload)


def write_json(path: Path, data: object) -> None:
    """Escribe JSON (indent 2, UTF-8, ensure_ascii False).

    Lanza :class:`RunArtifactExistsError` si el archivo ya existe.
    Crea los directorios padre si faltan.
    """
    text = json.dumps(data, indent=2, ensure_ascii=False)
    _write_bytes(path, text.encode("utf-8"))


def write_text(path: Path, text: str) -> None:
    """Escribe texto plano UTF-8 con la misma protección de write_json."""
    _write_bytes(path, text.encode("utf-8"))


def write_image_index(run_dir: Path, entries: list[dict]) -> None:
    """Escribe ``indice_imagenes.json`` dentro de ``run_dir``.

    Cada entry debe ser un dict con las claves:

    - ``archivo``: nombre del archivo de imagen (str).
    - ``tiempo_solicitado_s``: tiempo solicitado en segundos (float).
    - ``timestamp_real_s``: timestamp real extraído del video (float).
    - ``dimensiones``: par ``[ancho, alto]`` en píxeles.
    - ``transformaciones``: lista de transformaciones aplicadas (str).
    """
    write_json(run_dir / IMAGE_INDEX_FILENAME, entries)


def write_run_record(run_dir: Path, record: dict) -> None:
    """Escribe ``registro.json`` dentro de ``run_dir``.

    El registro debe incluir al menos las claves:

    - ``entrada``: dict con ``archivo`` y ``sha256`` del video original.
    - ``configuracion``: parámetros usados en la ejecución (dict).
    - ``versiones``: versiones de herramientas relevantes (dict).
    - ``comando``: comando ejecutado (str).
    - ``notas``: observaciones de la ejecución (str o lista).
    """
    write_json(run_dir / RUN_RECORD_FILENAME, record)
