import pytest
from zai_coder.cli import cmd_doctor
from argparse import Namespace
from pathlib import Path
import os

def test_cmd_doctor_runs(capsys, monkeypatch):
    # Mock ensure_config and load_config to return a simple config object
    class MockConfig:
        provider = "ollama"
        base_url = "http://localhost:11434"
        workspace = "."
        def to_dict(self):
            return {"provider": "ollama"}

    monkeypatch.setattr("zai_coder.cli.ensure_config", lambda c: Path("config.json"))
    monkeypatch.setattr("zai_coder.cli.load_config", lambda p: MockConfig())
    
    # Run doctor
    args = Namespace(config="config.json")
    ret = cmd_doctor(args)
    
    assert ret == 0
    captured = capsys.readouterr()
    assert "== Config ==" in captured.out
    assert "== Python ==" in captured.out
    assert "== Platform ==" in captured.out
    assert "== Workspace Status ==" in captured.out
