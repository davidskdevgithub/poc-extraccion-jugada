"""Tests del módulo de extracción de imágenes de referencia (E0)."""

import shutil
from pathlib import Path

import pytest

from jugadas_video.runs import RunArtifactExistsError
from jugadas_video.video.extract import (
    ExtractionError,
    FrameNotAvailableError,
    closest_frame_in_interval,
    extract_frame,
    extract_reference_frames,
    select_timestamps,
    snap_to_frame,
)
from jugadas_video.video.tools import run_tool

FFMPEG_AVAILABLE = shutil.which("ffmpeg") is not None
FFPROBE_AVAILABLE = shutil.which("ffprobe") is not None

pytestmark = [
    pytest.mark.skipif(
        not FFMPEG_AVAILABLE, reason="ffmpeg no está disponible"
    ),
    pytest.mark.skipif(
        not FFPROBE_AVAILABLE, reason="ffprobe no está disponible"
    ),
]

START = 0.0
END = 2.0


@pytest.fixture(scope="session")
def synthetic_video(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """Video sintético 320x240 a 10 fps durante 2 s (20 frames)."""
    out_path = tmp_path_factory.mktemp("video") / "sintetico.mp4"
    run_tool(
        [
            "ffmpeg",
            "-f",
            "lavfi",
            "-i",
            "testsrc=duration=2:size=320x240:rate=10",
            "-pix_fmt",
            "yuv420p",
            "-y",
            str(out_path),
        ]
    )
    return out_path


class TestSelectTimestamps:
    def test_intervalo_0_8_count_8_excluye_end(self) -> None:
        stamps = select_timestamps(0.0, 8.0, count=8)
        assert len(stamps) == 8
        assert stamps[0] == 0.0
        assert 8.0 not in stamps
        assert all(t < 8.0 for t in stamps)

    def test_es_determinista(self) -> None:
        assert select_timestamps(0.0, 8.0, count=8) == select_timestamps(
            0.0, 8.0, count=8
        )

    def test_regla_de_muestreo(self) -> None:
        stamps = select_timestamps(0.0, 2.0, count=4)
        assert stamps == [0.0, 0.5, 1.0, 1.5]

    def test_count_menor_a_1_lanza_error(self) -> None:
        with pytest.raises(ExtractionError, match="count"):
            select_timestamps(0.0, 2.0, count=0)

    def test_intervalo_invalido_lanza_error(self) -> None:
        from jugadas_video.validation import InvalidIntervalError

        with pytest.raises(InvalidIntervalError):
            select_timestamps(2.0, 2.0, count=4)


class TestClosestFrameInInterval:
    TIMESTAMPS = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5]

    def test_elige_el_frame_mas_cercano(self) -> None:
        ts = closest_frame_in_interval(self.TIMESTAMPS, 0.27, 0.0, 2.0)
        assert ts == 0.3

    def test_empate_elige_el_anterior(self) -> None:
        # 0.27 está a igual distancia de 0.2 y 0.3... usamos 0.25.
        ts = closest_frame_in_interval(self.TIMESTAMPS, 0.25, 0.0, 2.0)
        assert ts == 0.2

    def test_ignora_frames_fuera_del_intervalo(self) -> None:
        ts = closest_frame_in_interval([0.0, 0.1, 5.0, 9.0], 9.0, 0.0, 2.0)
        assert ts == 0.1

    def test_sin_frames_elegibles_lanza_error(self) -> None:
        with pytest.raises(FrameNotAvailableError, match="intervalo"):
            closest_frame_in_interval([5.0, 9.0], 1.0, 0.0, 2.0)

    def test_lista_vacia_lanza_error(self) -> None:
        with pytest.raises(FrameNotAvailableError):
            closest_frame_in_interval([], 1.0, 0.0, 2.0)


class TestSnapToFrame:
    def test_snap_al_frame_real_mas_cercano(
        self, synthetic_video: Path
    ) -> None:
        # Frames reales del sintético: 0.0, 0.1, ..., 1.9.
        ts = snap_to_frame(synthetic_video, 0.44, START, END)
        assert ts == pytest.approx(0.4)

    def test_snap_a_start_devuelve_el_primer_frame(
        self, synthetic_video: Path
    ) -> None:
        ts = snap_to_frame(synthetic_video, 0.0, START, END)
        assert ts == pytest.approx(0.0)

    def test_intervalo_sin_frames_lanza_error(
        self, synthetic_video: Path
    ) -> None:
        # El video dura 2 s; no hay frames después de 1.9.
        with pytest.raises(FrameNotAvailableError):
            snap_to_frame(synthetic_video, 1.95, 1.95, 1.99)


class TestExtractFrame:
    def test_png_con_dimensiones_correctas(
        self, synthetic_video: Path, tmp_path: Path
    ) -> None:
        out_path = tmp_path / "frame_t_0.000.png"
        entry = extract_frame(synthetic_video, 0.0, out_path)
        assert out_path.exists()
        assert entry["archivo"] == "frame_t_0.000.png"
        assert entry["dimensiones"] == [320, 240]
        assert entry["transformaciones"] == []

    def test_timestamp_real_dentro_del_intervalo(
        self, synthetic_video: Path, tmp_path: Path
    ) -> None:
        out_path = tmp_path / "frame.png"
        entry = extract_frame(synthetic_video, 0.5, out_path)
        assert START <= entry["timestamp_real_s"] <= END

    def test_out_path_existente_lanza_error(
        self, synthetic_video: Path, tmp_path: Path
    ) -> None:
        out_path = tmp_path / "frame.png"
        extract_frame(synthetic_video, 0.0, out_path)
        with pytest.raises(RunArtifactExistsError):
            extract_frame(synthetic_video, 0.0, out_path)


class TestExtractReferenceFrames:
    def test_produce_n_entries_y_archivos(
        self, synthetic_video: Path, tmp_path: Path
    ) -> None:
        requested = select_timestamps(START, END, count=4)
        out_dir = tmp_path / "run"
        entries = extract_reference_frames(
            synthetic_video, requested, out_dir, START, END
        )
        assert len(entries) == 4
        for entry in entries:
            assert START <= entry["timestamp_real_s"] <= END
            assert (out_dir / entry["archivo"]).exists()
        assert all(entry["transformaciones"] == [] for entry in entries)

    def test_con_reducidas_duplica_entries(
        self, synthetic_video: Path, tmp_path: Path
    ) -> None:
        requested = select_timestamps(START, END, count=2)
        out_dir = tmp_path / "run"
        entries = extract_reference_frames(
            synthetic_video,
            requested,
            out_dir,
            START,
            END,
            reduced_max_width=160,
        )
        assert len(entries) == 4
        reducidas = [entry for entry in entries if entry["transformaciones"]]
        assert len(reducidas) == 2
        for entry in reducidas:
            assert entry["transformaciones"] == ["escala a ancho max 160"]
            assert entry["archivo"].endswith("_reducida.png")
            assert (out_dir / entry["archivo"]).exists()
            assert entry["dimensiones"][0] <= 160
        for entry in entries:
            assert START <= entry["timestamp_real_s"] <= END

    def test_nombres_deterministas(
        self, synthetic_video: Path, tmp_path: Path
    ) -> None:
        requested = select_timestamps(START, END, count=2)
        out_dir = tmp_path / "run"
        entries = extract_reference_frames(
            synthetic_video, requested, out_dir, START, END
        )
        nombres = [entry["archivo"] for entry in entries]
        assert nombres == [
            f"frame_t_{entry['timestamp_real_s']:.3f}.png" for entry in entries
        ]

    def test_video_invalido_lanza_error(self, tmp_path: Path) -> None:
        from jugadas_video.validation import InvalidVideoFileError

        fake = tmp_path / "fake.mp4"
        fake.write_bytes(b"no es un mp4" * 100)
        with pytest.raises(InvalidVideoFileError):
            extract_reference_frames(fake, [0.0], tmp_path, START, END)
