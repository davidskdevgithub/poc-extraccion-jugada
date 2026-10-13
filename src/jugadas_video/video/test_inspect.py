"""Tests del módulo de inspección de video (UC-02, UC-E2, UC-E4)."""

import shutil
import subprocess
from pathlib import Path
from typing import Callable

import pytest

from jugadas_video.validation import InvalidIntervalError, InvalidVideoFileError
from jugadas_video.video import inspect
from jugadas_video.video.inspect import (
    InspectionError,
    ffprobe_json,
    frame_timestamps,
    inspect_file,
    temporal_summary,
)

FFMPEG = shutil.which("ffmpeg")
FFPROBE = shutil.which("ffprobe")

REQUIERE_FFMPEG = pytest.mark.skipif(
    FFMPEG is None or FFPROBE is None,
    reason="requiere ffmpeg y ffprobe en el PATH (UC-E1)",
)


@pytest.fixture(scope="session")
def video_sintetico(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """Genera UN video sintético de 2 s a 10 fps con ffmpeg (UC-E1)."""
    if FFMPEG is None or FFPROBE is None:
        pytest.skip("ffmpeg/ffprobe no disponibles (UC-E1)")
    destino = tmp_path_factory.mktemp("sintetico") / "sintetico.mp4"
    subprocess.run(
        [
            FFMPEG,
            "-f",
            "lavfi",
            "-i",
            "testsrc=duration=2:size=320x240:rate=10",
            "-pix_fmt",
            "yuv420p",
            "-y",
            str(destino),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return destino


def _fake_mp4(tmp_path: Path, name: str = "falso.mp4") -> Path:
    """Archivo con la firma MP4/ISO-BMFF mínima para pasar la validación."""
    path = tmp_path / name
    path.write_bytes(b"\x00\x00\x00\x18ftypisom\x00\x00\x02\x00" + b"\x00" * 8)
    return path


def _stream_video(**overrides: object) -> dict:
    stream: dict = {
        "codec_type": "video",
        "codec_name": "h264",
        "width": 320,
        "height": 240,
        "avg_frame_rate": "10/1",
        "time_base": "1/10000",
        "duration": "2.000000",
    }
    stream.update(overrides)
    return stream


def _probe(streams: list[dict], duration: str = "2.000000") -> dict:
    return {"streams": streams, "format": {"duration": duration}}


def _mock_probe(
    monkeypatch: pytest.MonkeyPatch, data: dict, raw: str = "{}"
) -> None:
    monkeypatch.setattr(inspect, "ffprobe_json", lambda _path: (data, raw))


def _mock_frames(
    monkeypatch: pytest.MonkeyPatch,
    timestamps: list[float],
    skipped: int = 0,
) -> None:
    monkeypatch.setattr(
        inspect,
        "_video_frame_timestamps",
        lambda _path: (timestamps, skipped),
    )


@REQUIERE_FFMPEG
class TestInspectFileIntegracion:
    def test_resumen_del_video_sintetico(self, video_sintetico: Path) -> None:
        resumen = inspect_file(video_sintetico)
        assert resumen["duracion_reportada_s"] == pytest.approx(2.0, abs=0.2)
        assert isinstance(resumen["codec"], str) and resumen["codec"]
        assert resumen["fps_nominal"] == pytest.approx(10.0, rel=0.01)
        assert resumen["ancho"] == 320
        assert resumen["alto"] == 240
        assert resumen["rotacion_grados"] is None
        assert isinstance(resumen["time_base"], str) and resumen["time_base"]
        assert resumen["indeterminados"] == []

    def test_ffprobe_json_devuelve_texto_crudo(
        self, video_sintetico: Path
    ) -> None:
        data, raw = ffprobe_json(video_sintetico)
        assert "streams" in data
        assert '"streams"' in raw

    def test_frame_timestamps_solo_del_intervalo(
        self, video_sintetico: Path
    ) -> None:
        ts = frame_timestamps(video_sintetico, 0.5, 1.5)
        assert ts, "debe haber frames en [0.5, 1.5]"
        assert all(0.5 <= t <= 1.5 for t in ts)
        assert ts == sorted(ts)
        # 10 fps: frames en 0.5, 0.6, ..., 1.5 → 11 timestamps.
        assert len(ts) == 11

    def test_frame_timestamps_intervalo_invalido(
        self, video_sintetico: Path
    ) -> None:
        with pytest.raises(InvalidIntervalError):
            frame_timestamps(video_sintetico, 1.5, 0.5)

    def test_temporal_summary_del_video_sintetico(
        self, video_sintetico: Path
    ) -> None:
        resumen = temporal_summary(video_sintetico, 0.5, 1.5)
        assert resumen["intervalo"] == [0.5, 1.5]
        assert resumen["n_frames"] == 11
        assert resumen["fps_efectivo"] == pytest.approx(10.0, rel=0.01)
        assert resumen["fps_variable"] is False
        assert resumen["primer_frame_s"] == pytest.approx(0.5, abs=1e-9)
        assert resumen["ultimo_frame_s"] == pytest.approx(1.5, abs=1e-9)
        assert resumen["indeterminados"] == []


class TestArchivoInvalido:
    """UC-E2: la validación rechaza antes de invocar ffprobe."""

    @staticmethod
    def _prohibir_ffprobe(monkeypatch: pytest.MonkeyPatch) -> None:
        def _fallar(_path: object) -> tuple[dict, str]:
            raise AssertionError("ffprobe_json no debía invocarse")

        monkeypatch.setattr(inspect, "ffprobe_json", _fallar)

    def test_inspect_file_rechaza_archivo_de_texto(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        archivo = tmp_path / "no-video.txt"
        archivo.write_text("esto no es un video", encoding="utf-8")
        self._prohibir_ffprobe(monkeypatch)
        with pytest.raises(InvalidVideoFileError):
            inspect_file(archivo)

    def test_temporal_summary_rechaza_archivo_de_texto(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        archivo = tmp_path / "no-video.txt"
        archivo.write_text("esto no es un video", encoding="utf-8")
        self._prohibir_ffprobe(monkeypatch)
        with pytest.raises(InvalidVideoFileError):
            temporal_summary(archivo, 0.0, 1.0)


class TestNormalizacionMetadatos:
    """UC-E4: normalización con salidas sintéticas de ffprobe."""

    def test_avg_frame_rate_0_0_es_indeterminado(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        _mock_probe(monkeypatch, _probe([_stream_video(avg_frame_rate="0/0")]))
        resumen = inspect_file(_fake_mp4(tmp_path))
        assert resumen["fps_nominal"] is None
        assert any("avg_frame_rate" in msg for msg in resumen["indeterminados"])

    def test_avg_frame_rate_ausente_es_indeterminado(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        stream = _stream_video()
        del stream["avg_frame_rate"]
        _mock_probe(monkeypatch, _probe([stream]))
        resumen = inspect_file(_fake_mp4(tmp_path))
        assert resumen["fps_nominal"] is None
        assert resumen["indeterminados"]

    def test_avg_frame_rate_fraccion_no_entera(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        _mock_probe(
            monkeypatch,
            _probe([_stream_video(avg_frame_rate="30000/1001")]),
        )
        resumen = inspect_file(_fake_mp4(tmp_path))
        assert resumen["fps_nominal"] == pytest.approx(29.97, rel=1e-3)
        assert resumen["indeterminados"] == []

    def test_sin_rotacion_devuelve_none(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        _mock_probe(monkeypatch, _probe([_stream_video()]))
        resumen = inspect_file(_fake_mp4(tmp_path))
        assert resumen["rotacion_grados"] is None

    def test_rotacion_por_tag_rotate(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        _mock_probe(
            monkeypatch,
            _probe([_stream_video(tags={"rotate": "90"})]),
        )
        resumen = inspect_file(_fake_mp4(tmp_path))
        assert resumen["rotacion_grados"] == 90.0

    def test_rotacion_por_side_data_displaymatrix(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        stream = _stream_video(
            side_data_list=[
                {
                    "side_data_type": "Display Matrix",
                    "displaymatrix:rotation": "-90",
                }
            ]
        )
        _mock_probe(monkeypatch, _probe([stream]))
        resumen = inspect_file(_fake_mp4(tmp_path))
        assert resumen["rotacion_grados"] == -90.0

    def test_duracion_ausente_es_indeterminada(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        stream = _stream_video()
        del stream["duration"]
        data = _probe([stream], duration="")
        _mock_probe(monkeypatch, data)
        resumen = inspect_file(_fake_mp4(tmp_path))
        assert resumen["duracion_reportada_s"] is None
        assert any(
            "duracion_reportada_s" in msg for msg in resumen["indeterminados"]
        )

    def test_json_sin_streams_de_video_lanza_inspection_error(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        _mock_probe(monkeypatch, _probe([]))
        with pytest.raises(InspectionError, match="UC-E2"):
            inspect_file(_fake_mp4(tmp_path))

    def test_json_sin_clave_streams_lanza_inspection_error(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        _mock_probe(monkeypatch, {"format": {"duration": "2.000000"}})
        with pytest.raises(InspectionError, match="UC-E2"):
            inspect_file(_fake_mp4(tmp_path))


class TestMetricasTemporales:
    def test_timestamps_uniformes_variable_false(self) -> None:
        ts = [i * 0.1 for i in range(10)]
        fps, variable, notas = inspect._compute_temporal_metrics(ts, 10.0)
        assert fps == pytest.approx(10.0, rel=1e-9)
        assert variable is False
        assert notas == []

    def test_timestamps_con_huecos_variable_true(self) -> None:
        # Falta el frame en 0.3: el gap de 0.2 delata el hueco (UC-E4).
        ts = [0.0, 0.1, 0.2, 0.4, 0.5]
        fps, variable, notas = inspect._compute_temporal_metrics(ts, 10.0)
        assert variable is True
        assert fps == pytest.approx(8.0, rel=1e-9)
        assert notas == []

    def test_hueco_con_fps_nominal_ausente(self) -> None:
        ts = [0.0, 0.1, 0.3]
        _fps, variable, _notas = inspect._compute_temporal_metrics(ts, None)
        assert variable is True

    def test_menos_de_dos_frames_no_determina_nada(self) -> None:
        fps, variable, notas = inspect._compute_temporal_metrics([0.5], 10.0)
        assert fps is None
        assert variable is None
        assert notas == []


class TestTemporalSummaryUnit:
    def test_huecos_marcan_fps_variable(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        _mock_frames(monkeypatch, [0.0, 0.1, 0.2, 0.4, 0.5, 0.6])
        _mock_probe(monkeypatch, _probe([_stream_video()]))
        resumen = temporal_summary(_fake_mp4(tmp_path), 0.0, 1.0)
        assert resumen["intervalo"] == [0.0, 1.0]
        assert resumen["n_frames"] == 6
        assert resumen["fps_variable"] is True
        assert resumen["primer_frame_s"] == 0.0
        assert resumen["ultimo_frame_s"] == 0.6

    def test_intervalo_sin_frames_no_es_error(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        _mock_frames(monkeypatch, [0.0, 0.1])
        _mock_probe(monkeypatch, _probe([_stream_video()]))
        resumen = temporal_summary(_fake_mp4(tmp_path), 5.0, 6.0)
        assert resumen["n_frames"] == 0
        assert resumen["fps_efectivo"] is None
        assert resumen["fps_variable"] is None
        assert resumen["primer_frame_s"] is None
        assert resumen["ultimo_frame_s"] is None
        assert any("no hay frames" in msg for msg in resumen["indeterminados"])

    def test_frames_sin_pts_time_se_registran(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        _mock_frames(monkeypatch, [0.0, 0.2], skipped=1)
        _mock_probe(monkeypatch, _probe([_stream_video()]))
        resumen = temporal_summary(_fake_mp4(tmp_path), 0.0, 1.0)
        assert resumen["n_frames"] == 2
        assert any("omitido" in msg for msg in resumen["indeterminados"])

    def test_intervalo_invalido_se_rechaza(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        llamado: list[Callable] = []

        def _no_llamar(*_args: object) -> None:
            llamado.append(_no_llamar)

        monkeypatch.setattr(inspect, "_video_frame_timestamps", _no_llamar)
        with pytest.raises(InvalidIntervalError):
            temporal_summary(_fake_mp4(tmp_path), -1.0, 1.0)
        assert llamado == []
