"""Tests unitarios para las validaciones de la etapa E0."""

import math
import struct

import pytest

from jugadas_video.validation import (
    InvalidIntervalError,
    InvalidVideoFileError,
    ValidationError,
    validate_interval,
    validate_video_file,
)

# ---------------------------------------------------------------
# validate_interval
# ---------------------------------------------------------------


class TestValidateInterval:
    def test_intervalo_valido(self) -> None:
        assert validate_interval(0.0, 10.0) == (0.0, 10.0)

    def test_normaliza_enteros_a_float(self) -> None:
        assert validate_interval(1, 5) == (1.0, 5.0)

    @pytest.mark.parametrize(
        "value", [float("nan"), float("inf"), float("-inf")]
    )
    def test_start_no_finito(self, value: float) -> None:
        with pytest.raises(InvalidIntervalError, match="start"):
            validate_interval(value, 10.0)

    @pytest.mark.parametrize(
        "value", [float("nan"), float("inf"), float("-inf")]
    )
    def test_end_no_finito(self, value: float) -> None:
        with pytest.raises(InvalidIntervalError, match="end"):
            validate_interval(0.0, value)

    @pytest.mark.parametrize("start", [-0.1, -1.0, -1e9])
    def test_start_negativo(self, start: float) -> None:
        with pytest.raises(InvalidIntervalError, match="negativo"):
            validate_interval(start, 10.0)

    def test_start_cero_es_valido(self) -> None:
        assert validate_interval(0.0, 5.0) == (0.0, 5.0)

    @pytest.mark.parametrize(
        ("start", "end"),
        [(5.0, 5.0), (10.0, 1.0), (3.0, 3.0 - 1e-9)],
    )
    def test_end_menor_o_igual_a_start(self, start: float, end: float) -> None:
        with pytest.raises(InvalidIntervalError, match="mayor que"):
            validate_interval(start, end)

    def test_excede_duracion_conocida(self) -> None:
        with pytest.raises(InvalidIntervalError, match="excede"):
            validate_interval(0.0, 11.0, known_duration=10.0)

    def test_exceso_se_indica_en_el_mensaje(self) -> None:
        with pytest.raises(InvalidIntervalError, match="1\\.5 s"):
            validate_interval(0.0, 11.5, known_duration=10.0)

    def test_end_igual_a_duracion_es_valido(self) -> None:
        assert validate_interval(5.0, 10.0, known_duration=10.0) == (5.0, 10.0)

    def test_duracion_none_no_valida_limite_superior(self) -> None:
        assert validate_interval(0.0, 1e12, known_duration=None) == (0.0, 1e12)

    def test_hereda_de_validation_error(self) -> None:
        assert issubclass(InvalidIntervalError, ValidationError)
        assert issubclass(InvalidVideoFileError, ValidationError)

    def test_nan_no_confundible_con_start_negativo(self) -> None:
        # NaN es rechazado por no finito antes que por cualquier otra regla.
        with pytest.raises(InvalidIntervalError) as excinfo:
            validate_interval(math.nan, 5.0)
        assert "finito" in str(excinfo.value)


# ---------------------------------------------------------------
# validate_video_file
# ---------------------------------------------------------------


def _write_mp4_header(path, brand: bytes = b"isom") -> None:
    """Escribe los primeros bytes de un contenedor MP4/ISO-BMFF."""
    # major_brand + minor_version + marcas de compatibilidad de relleno.
    payload = brand + b"\x00\x00\x02\x00" + b"mp41isomiso2"
    box_size = 8 + len(payload)
    path.write_bytes(struct.pack(">I", box_size) + b"ftyp" + payload)


class TestValidateVideoFile:
    def test_archivo_inexistente(self, tmp_path) -> None:
        target = tmp_path / "no_existe.mp4"
        with pytest.raises(InvalidVideoFileError, match="no existe"):
            validate_video_file(target)

    def test_directorio_no_es_archivo_regular(self, tmp_path) -> None:
        with pytest.raises(InvalidVideoFileError, match="archivo regular"):
            validate_video_file(tmp_path)

    def test_archivo_vacio(self, tmp_path) -> None:
        target = tmp_path / "vacio.mp4"
        target.write_bytes(b"")
        with pytest.raises(InvalidVideoFileError, match="vacío"):
            validate_video_file(target)

    def test_sin_firma_ftyp(self, tmp_path) -> None:
        target = tmp_path / "sin_firma.mp4"
        target.write_bytes(b"RIFFxxxxWAVEfmt " + b"\x00" * 4)
        with pytest.raises(InvalidVideoFileError, match="ftyp"):
            validate_video_file(target)

    def test_menor_de_12_bytes_con_ftyp_al_comienzo(self, tmp_path) -> None:
        target = tmp_path / "corto.mp4"
        target.write_bytes(b"\x00\x00\x00\x08ftyp")
        with pytest.raises(InvalidVideoFileError, match="ftyp"):
            validate_video_file(target)

    def test_ftyp_en_offset_incorrecto(self, tmp_path) -> None:
        target = tmp_path / "offset_mal.mp4"
        target.write_bytes(b"abcftyp" + b"\x00" * 8)
        with pytest.raises(InvalidVideoFileError, match="ftyp"):
            validate_video_file(target)

    def test_archivo_mp4_valido(self, tmp_path) -> None:
        target = tmp_path / "video.mp4"
        _write_mp4_header(target)
        assert validate_video_file(target) == target.resolve()

    def test_resuelve_la_ruta(self, tmp_path) -> None:
        target = tmp_path / "video.mp4"
        _write_mp4_header(target)
        relativo = tmp_path / "." / "video.mp4"
        assert validate_video_file(relativo) == target.resolve()

    def test_hereda_de_validation_error(self) -> None:
        assert issubclass(InvalidVideoFileError, ValidationError)
