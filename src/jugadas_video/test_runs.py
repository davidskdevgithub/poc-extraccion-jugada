"""Tests del módulo de gestión de ejecuciones de E0."""

import hashlib
import json
from pathlib import Path

import pytest

from jugadas_video.runs import (
    IMAGE_INDEX_FILENAME,
    RUN_RECORD_FILENAME,
    RunArtifactExistsError,
    create_run_dir,
    sha256_file,
    write_image_index,
    write_json,
    write_run_record,
    write_text,
)


class TestSha256File:
    def test_hash_de_archivo_conocido(self, tmp_path: Path) -> None:
        target = tmp_path / "entrada.mp4"
        target.write_bytes(b"contenido de prueba")
        expected = hashlib.sha256(b"contenido de prueba").hexdigest()
        assert sha256_file(target) == expected

    def test_hash_vacio_y_bloques(self, tmp_path: Path) -> None:
        vacio = tmp_path / "vacio.bin"
        vacio.write_bytes(b"")
        assert sha256_file(vacio) == hashlib.sha256(b"").hexdigest()

        grande = tmp_path / "grande.bin"
        grande.write_bytes(b"x" * (3 * 1024 * 1024 + 17))
        assert (
            sha256_file(grande)
            == hashlib.sha256(b"x" * (3 * 1024 * 1024 + 17)).hexdigest()
        )


class TestCreateRunDir:
    def test_crea_jerarquia_y_devuelve_path(self, tmp_path: Path) -> None:
        run_dir = create_run_dir("e0", base_dir=tmp_path)
        assert run_dir.parent == tmp_path / "e0"
        assert run_dir.is_dir()
        # run-id con formato YYYYMMDD-HHMMSS
        assert len(run_dir.name) == 15
        assert run_dir.name[8] == "-"

    def test_llamadas_sucesivas_sin_colision(self, tmp_path: Path) -> None:
        first = create_run_dir("e0", base_dir=tmp_path)
        second = create_run_dir("e0", base_dir=tmp_path)
        third = create_run_dir("e0", base_dir=tmp_path)
        paths = {first, second, third}
        assert len(paths) == 3
        for run_dir in paths:
            assert run_dir.is_dir()

    def test_respeta_run_id_existente_con_sufijo(self, tmp_path: Path) -> None:
        stage_dir = tmp_path / "e0"
        stage_dir.mkdir(parents=True)
        existing = stage_dir / "20240101-120000"
        existing.mkdir()

        run_dir = create_run_dir("e0", base_dir=tmp_path)
        assert run_dir != existing
        assert run_dir.parent == stage_dir
        assert existing.is_dir()
        # Todos los run-id generados deben partir del mismo stamp
        # con sufijo numérico, nunca reutilizar el existente.
        assert run_dir.name.startswith("20")


class TestWriteJson:
    def test_escribe_json_valido(self, tmp_path: Path) -> None:
        target = tmp_path / "sub" / "datos.json"
        data = {"clave": "valor con áéíóú", "num": [1, 2, 3]}
        write_json(target, data)
        loaded = json.loads(target.read_text(encoding="utf-8"))
        assert loaded == data
        # indent 2 y ensure_ascii False
        text = target.read_text(encoding="utf-8")
        assert '\n  "clave"' in text
        assert "áéíóú" in text

    def test_rechaza_sobrescribir(self, tmp_path: Path) -> None:
        target = tmp_path / "datos.json"
        write_json(target, {"a": 1})
        with pytest.raises(RunArtifactExistsError):
            write_json(target, {"a": 2})
        assert json.loads(target.read_text(encoding="utf-8")) == {"a": 1}


class TestWriteText:
    def test_escribe_texto_utf8(self, tmp_path: Path) -> None:
        target = tmp_path / "sub" / "notas.txt"
        write_text(target, "nota con ñ y ü")
        assert target.read_text(encoding="utf-8") == "nota con ñ y ü"

    def test_rechaza_sobrescribir(self, tmp_path: Path) -> None:
        target = tmp_path / "notas.txt"
        write_text(target, "primera")
        with pytest.raises(RunArtifactExistsError):
            write_text(target, "segunda")
        assert target.read_text(encoding="utf-8") == "primera"


class TestWriteImageIndex:
    def test_escribe_indice_con_claves_esperadas(self, tmp_path: Path) -> None:
        entries = [
            {
                "archivo": "f000001.jpg",
                "tiempo_solicitado_s": 0.0,
                "timestamp_real_s": 0.0,
                "dimensiones": [1920, 1080],
                "transformaciones": ["resize", "pad"],
            },
            {
                "archivo": "f000002.jpg",
                "tiempo_solicitado_s": 1.5,
                "timestamp_real_s": 1.533,
                "dimensiones": [1920, 1080],
                "transformaciones": [],
            },
        ]
        write_image_index(tmp_path, entries)
        target = tmp_path / IMAGE_INDEX_FILENAME
        assert target.is_file()
        loaded = json.loads(target.read_text(encoding="utf-8"))
        assert loaded == entries
        for entry in loaded:
            assert set(entry) == {
                "archivo",
                "tiempo_solicitado_s",
                "timestamp_real_s",
                "dimensiones",
                "transformaciones",
            }


class TestWriteRunRecord:
    def test_escribe_registro_con_claves_minimas(self, tmp_path: Path) -> None:
        record = {
            "entrada": {"archivo": "video.mp4", "sha256": "abc123"},
            "configuracion": {"fps": 2.0, "scale": 1.0},
            "versiones": {"ffmpeg": "7.1", "opencv": "4.10"},
            "comando": "python -m jugadas_video.extraer --fps 2",
            "notas": "sin incidencias",
        }
        write_run_record(tmp_path, record)
        target = tmp_path / RUN_RECORD_FILENAME
        assert target.is_file()
        loaded = json.loads(target.read_text(encoding="utf-8"))
        assert loaded == record
        for key in (
            "entrada",
            "configuracion",
            "versiones",
            "comando",
            "notas",
        ):
            assert key in loaded
        assert "sha256" in loaded["entrada"]
        assert "archivo" in loaded["entrada"]
