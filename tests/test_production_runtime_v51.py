"""v51 Production Runtime Gate — tests."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from zai_coder.production_runtime.gate import (
    check_asgi_import,
    check_health_probes,
    check_production_deps,
    run_runtime_gate,
)


# ---------------------------------------------------------------------------
# check_production_deps
# ---------------------------------------------------------------------------

def test_check_production_deps_present():
    """All production packages should be importable in the test environment
    OR the check should return a graceful failure message — never raise."""
    result = check_production_deps()
    assert isinstance(result, dict)
    assert "ok" in result
    assert "message" in result
    assert isinstance(result["ok"], bool)


def test_check_production_deps_missing(monkeypatch):
    """Simulate a missing package and verify ok=False + helpful message."""
    import importlib.util as ilu

    original_find_spec = ilu.find_spec

    def fake_find_spec(name, *args, **kwargs):
        if name == "fastapi":
            return None
        return original_find_spec(name, *args, **kwargs)

    monkeypatch.setattr(ilu, "find_spec", fake_find_spec)
    result = check_production_deps()
    assert result["ok"] is False
    assert "fastapi" in result["message"]


# ---------------------------------------------------------------------------
# check_asgi_import
# ---------------------------------------------------------------------------

def test_check_asgi_import_structure():
    """check_asgi_import should always return ok/message dict."""
    result = check_asgi_import()
    assert isinstance(result, dict)
    assert "ok" in result
    assert "message" in result


def test_check_asgi_import_when_uvicorn_missing(monkeypatch):
    """Simulate uvicorn absent — should return ok=True (graceful), uvicorn_available=False."""
    import builtins

    real_import = builtins.__import__

    def fake_import(name, *args, **kwargs):
        if name == "uvicorn":
            raise ImportError("No module named 'uvicorn'")
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", fake_import)
    result = check_asgi_import()
    # Graceful: ok must be True even when uvicorn is absent
    assert result["ok"] is True
    assert result.get("uvicorn_available") is False
    assert "uvicorn" in result["message"]


# ---------------------------------------------------------------------------
# check_health_probes
# ---------------------------------------------------------------------------

def test_check_health_probes_advisory_when_server_down():
    """When no server is running, probes should return ok=True (advisory)."""
    result = check_health_probes(host="127.0.0.1", port=9999)
    assert isinstance(result, dict)
    assert "ok" in result
    assert result["ok"] is True  # advisory, not a hard failure


def test_check_health_probes_returns_probes_key():
    """Result should always contain a 'probes' key."""
    result = check_health_probes(host="127.0.0.1", port=9999)
    assert "probes" in result
    # probes may be a dict or list depending on implementation
    assert isinstance(result["probes"], (dict, list))


def test_check_health_probes_with_running_server(monkeypatch):
    """Simulate a responding server and verify ok=True with reachable status."""
    mock_result = MagicMock()
    mock_result.returncode = 0

    with patch("subprocess.run", return_value=mock_result):
        result = check_health_probes(host="127.0.0.1", port=8765)

    assert result["ok"] is True
    assert "reachable" in result["message"].lower()


# ---------------------------------------------------------------------------
# run_runtime_gate
# ---------------------------------------------------------------------------

def test_run_runtime_gate_structure():
    """Gate report should have ok, gate, checks, and message keys."""
    report = run_runtime_gate()
    assert isinstance(report, dict)
    assert "ok" in report
    assert "gate" in report
    assert "checks" in report
    assert "message" in report
    assert report["gate"] == "v51-production-runtime"


def test_run_runtime_gate_checks_contain_all_areas():
    """Gate report should contain production_deps, asgi_import, health_probes."""
    report = run_runtime_gate()
    checks = report["checks"]
    assert "production_deps" in checks
    assert "asgi_import" in checks
    assert "health_probes" in checks


def test_run_runtime_gate_serializable():
    """Gate report must be JSON-serializable for CI output."""
    report = run_runtime_gate()
    serialized = json.dumps(report)
    parsed = json.loads(serialized)
    assert parsed["gate"] == "v51-production-runtime"


def test_run_runtime_gate_health_probes_advisory():
    """Gate should pass even when health probes return skipped (advisory)."""
    with patch(
        "zai_coder.production_runtime.gate.check_production_deps",
        return_value={"ok": True, "message": "ok"},
    ), patch(
        "zai_coder.production_runtime.gate.check_asgi_import",
        return_value={"ok": True, "message": "ok"},
    ), patch(
        "zai_coder.production_runtime.gate.check_health_probes",
        return_value={"ok": True, "message": "skipped", "probes": {}},
    ):
        report = run_runtime_gate()
    assert report["ok"] is True
