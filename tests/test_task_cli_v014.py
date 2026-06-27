from __future__ import annotations

import json

from zai_coder.cli import build_parser
from zai_coder.config import ZaiConfig


def _run_task_cli(tmp_path, monkeypatch, argv):
    monkeypatch.setattr("zai_coder.config.load_config", lambda path=None: ZaiConfig(workspace=str(tmp_path)))
    parser = build_parser()
    ns = parser.parse_args(["task", *argv])
    return ns.func(ns)


def test_task_cli_create_show_update_retry_export(tmp_path, monkeypatch, capsys):
    rc = _run_task_cli(tmp_path, monkeypatch, ["create", "--title", "build index", "--agent", "planner", "--prompt", "build the index"])
    assert rc == 0
    created = json.loads(capsys.readouterr().out)
    task_id = created["id"]

    rc = _run_task_cli(tmp_path, monkeypatch, ["show", str(task_id)])
    assert rc == 0
    shown = json.loads(capsys.readouterr().out)
    assert shown["title"] == "build index"

    rc = _run_task_cli(tmp_path, monkeypatch, ["update", str(task_id), "--state", "failed"])
    assert rc == 0
    updated = json.loads(capsys.readouterr().out)
    assert updated["state"] == "failed"

    rc = _run_task_cli(tmp_path, monkeypatch, ["retry", str(task_id)])
    assert rc == 0
    retried = json.loads(capsys.readouterr().out)
    assert retried["state"] == "queued"

    rc = _run_task_cli(tmp_path, monkeypatch, ["export", "--json"])
    assert rc == 0
    exported = json.loads(capsys.readouterr().out)
    assert exported["schema_version"]["name"] == "task_queue"
    assert exported["tasks"][0]["id"] == task_id


def test_task_cli_run_and_logs(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr("zai_coder.core.approvals.prompt_for_approval", lambda _: True)
    rc = _run_task_cli(tmp_path, monkeypatch, ["create", "--title", "execute", "--agent", "planner", "--prompt", "execute prompt"])
    assert rc == 0
    task_id = json.loads(capsys.readouterr().out)["id"]

    rc = _run_task_cli(tmp_path, monkeypatch, ["run", str(task_id), "--apply"])
    assert rc == 0
    result = json.loads(capsys.readouterr().out)
    assert result["state"] == "completed"

    rc = _run_task_cli(tmp_path, monkeypatch, ["logs", str(task_id)])
    assert rc == 0
    output = capsys.readouterr().out
    assert "START" in output.upper()
