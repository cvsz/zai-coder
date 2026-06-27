from __future__ import annotations

from io import BytesIO
from pathlib import Path
from types import SimpleNamespace

import pytest

from zai_coder.server.app import ZaiServerHandler
from zai_coder.server.http import JsonHTTPRequestHandler, MAX_REQUEST_SIZE
from zai_coder.server.routes import handle_get, handle_post


class CaptureHandler:
    def __init__(self, *, body: bytes | None = None, content_length: int | None = None):
        self.status_code = None
        self.payload = None
        self.headers = {}
        self.wfile = BytesIO()
        self.rfile = BytesIO(body or b"")
        if content_length is not None:
            self.headers["Content-Length"] = str(content_length)

    def send_response(self, status_code: int):
        self.status_code = status_code

    def send_header(self, name: str, value: str):
        self.headers[name] = value

    def end_headers(self):
        return None

    def send_json_response(self, status_code: int, data: dict):
        self.status_code = status_code
        self.payload = data


def test_health():
    handler = CaptureHandler()
    handle_get(handler, "/health")
    assert handler.status_code == 200
    assert handler.payload == {"status": "ok"}


def test_version():
    handler = CaptureHandler()
    handle_get(handler, "/version")
    assert handler.status_code == 200
    assert "version" in handler.payload


def test_agents():
    handler = CaptureHandler()
    handle_get(handler, "/agents")
    assert handler.status_code == 200
    assert isinstance(handler.payload["agents"], list)


def test_skills():
    handler = CaptureHandler()
    handle_get(handler, "/skills")
    assert handler.status_code == 200
    assert "skills" in handler.payload


def test_self_features():
    handler = CaptureHandler()
    handle_get(handler, "/self/features")
    assert handler.status_code == 200
    assert "features" in handler.payload


def test_self_status():
    handler = CaptureHandler()
    handle_get(handler, "/self/status")
    assert handler.status_code == 200
    assert "status" in handler.payload


def test_payload_too_large():
    body = b'{"text":"' + b"A" * 32 + b'"}'
    handler = CaptureHandler(body=body, content_length=MAX_REQUEST_SIZE + 1)
    body_result = JsonHTTPRequestHandler.read_json_body(handler)
    assert body_result is None
    assert handler.status_code == 413
    assert handler.payload == {"error": "Payload too large"}


def test_run_command_blocked(tmp_path, monkeypatch):
    fake_cfg = SimpleNamespace(
        workspace=str(tmp_path),
        allow_apps_zlms=False,
        tool_timeout_seconds=1,
    )

    class FakeToolRuntime:
        def __init__(self, **kwargs):
            self.kwargs = kwargs

        def run(self, command: str):
            return SimpleNamespace(
                exit_code=0,
                stdout="",
                stderr="",
                blocked_reason="blocked by safety policy",
            )

    monkeypatch.setattr("zai_coder.server.routes.load_config", lambda config_path: fake_cfg)
    monkeypatch.setattr("zai_coder.server.routes.ToolRuntime", FakeToolRuntime)

    handler = CaptureHandler()
    handle_post(handler, "/run", {"command": "rm -rf /"}, config_path=str(Path(tmp_path) / "config.json"))
    assert handler.status_code == 200
    assert "blocked_reason" in handler.payload
