"""Tests de la encapsulación de herramientas externas."""

import pytest

from jugadas_video.video.tools import (
    ExternalToolMissingError,
    VideoToolError,
    require_tool,
    run_tool,
)


class TestRequireTool:
    def test_herramienta_presente_devuelve_ruta(self) -> None:
        ruta = require_tool("python3")
        assert ruta

    def test_herramienta_ausente_lanza_error(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setattr("shutil.which", lambda name: None)
        with pytest.raises(ExternalToolMissingError, match="inexistente"):
            require_tool("inexistente-xyz")


class TestRunTool:
    def test_comando_exitoso(self) -> None:
        proc = run_tool(["python3", "-c", "print('ok')"])
        assert proc.returncode == 0
        assert "ok" in proc.stdout

    def test_comando_fallido_lanza_error(self) -> None:
        with pytest.raises(VideoToolError, match="código"):
            run_tool(["python3", "-c", "raise SystemExit(3)"])

    def test_ejecutable_ausente_lanza_error(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setattr("shutil.which", lambda name: None)
        with pytest.raises(ExternalToolMissingError):
            run_tool(["inexistente-xyz", "--version"])
