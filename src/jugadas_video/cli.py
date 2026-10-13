"""CLI mínima de la PoC (architecture.md §3.B).

Interpreta argumentos y llama a la lógica de los módulos; no contiene
lectura de video, transformaciones ni construcción de resultados.
"""

import argparse
import json
import sys
from pathlib import Path

from jugadas_video.runs import (
    create_run_dir,
    sha256_file,
    write_image_index,
    write_json,
    write_run_record,
    write_text,
)
from jugadas_video.validation import ValidationError, validate_interval
from jugadas_video.video.extract import (
    extract_reference_frames,
    select_timestamps,
)
from jugadas_video.video.inspect import (
    ffprobe_json,
    inspect_file,
    temporal_summary,
)
from jugadas_video.video.tools import (
    ExternalToolMissingError,
    VideoToolError,
    run_tool,
)


def _versiones() -> dict:
    """Versiones de las herramientas usadas (UC-01, UC-04)."""
    versiones = {"python": sys.version.split()[0]}
    bandera_version = {
        "ffmpeg": "-version",
        "ffprobe": "-version",
        "uv": "--version",
    }
    for nombre, bandera in bandera_version.items():
        try:
            proc = run_tool([nombre, bandera])
            versiones[nombre] = proc.stdout.splitlines()[0]
        except (ExternalToolMissingError, VideoToolError) as exc:
            versiones[nombre] = f"no disponible: {exc}"
    return versiones


def _registrar_medios(video: Path, data_dir: Path) -> dict:
    """Registra entrada y medios presentes en data/local (UC-G1)."""
    medios = [
        {"archivo": p.name, "bytes": p.stat().st_size}
        for p in sorted(data_dir.iterdir())
        if p.is_file()
    ]
    return {
        "archivo": str(video),
        "sha256": sha256_file(video),
        "medios_en_data_local": medios,
    }


def run_e0(args: argparse.Namespace) -> int:
    """Ejecuta la inspección y extracción de E0 en una corrida identificada."""
    video = Path(args.video)
    data_dir = Path(args.data_dir)
    start, end = validate_interval(args.start, args.end)

    run_dir = create_run_dir("e0", Path(args.base_dir))
    comando = f"python -m jugadas_video {' '.join(sys.argv[1:])}"
    notas: list[str] = []

    # Inspección (UC-02): salida cruda de ffprobe + resúmenes legibles.
    resumen = inspect_file(video)
    _data, crudo = ffprobe_json(video)
    write_text(run_dir / "ffprobe_salida_original.json", crudo)
    write_json(run_dir / "resumen_inspeccion.json", resumen)
    temporal = temporal_summary(video, start, end)
    write_json(run_dir / "resumen_temporal.json", temporal)

    # Extracción de referencias (UC-03): resolución original + reducidas.
    solicitados = select_timestamps(start, end, count=args.count)
    entries = extract_reference_frames(
        video,
        solicitados,
        run_dir / "imagenes",
        start,
        end,
        reduced_max_width=args.reduced_max_width,
    )
    write_image_index(run_dir, entries)

    # Registro de la ejecución (UC-04) al final: refleja una corrida
    # que llegó a producir todos sus artefactos.
    registro = {
        "entrada": _registrar_medios(video, data_dir),
        "configuracion": {
            "intervalo_s": [start, end],
            "frames_solicitados": args.count,
            "reducidas_ancho_max": args.reduced_max_width,
            "muestreo": "t_i = start + i * (end - start) / count, "
            "incluye start y excluye end",
        },
        "versiones": _versiones(),
        "comando": comando,
        "notas": notas,
    }
    write_run_record(run_dir, registro)

    print(
        json.dumps(
            {
                "run_dir": str(run_dir),
                "resumen_inspeccion": resumen,
                "resumen_temporal": temporal,
                "imagenes": len(entries),
            },
            indent=2,
            ensure_ascii=False,
        )
    )
    return 0


def main() -> int:
    """Punto de entrada de la CLI."""
    parser = argparse.ArgumentParser(prog="jugadas_video")
    sub = parser.add_subparsers(dest="comando", required=True)

    e0 = sub.add_parser(
        "e0", help="Inspección y extracción de referencias (E0)"
    )
    e0.add_argument("--video", default="data/local/gol-del-rival.mp4")
    e0.add_argument("--data-dir", default="data/local")
    e0.add_argument("--start", type=float, default=0.0)
    e0.add_argument("--end", type=float, default=8.0)
    e0.add_argument("--count", type=int, default=12)
    e0.add_argument("--reduced-max-width", type=int, default=1280)
    e0.add_argument("--base-dir", default="artifacts")
    e0.set_defaults(func=run_e0)

    args = parser.parse_args()
    try:
        return args.func(args)
    except (
        ValueError,
        OSError,
        ValidationError,
        RuntimeError,
    ) as exc:
        # Las excepciones de herramientas y módulos de video derivan de
        # RuntimeError: se informan de forma visible (architecture.md §3.J).
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
