from __future__ import annotations

import json

from zai_coder.cli import build_parser
from zai_coder.config import ZaiConfig
from zai_coder.core.artifacts import ArtifactStore, sha256_file


def test_artifact_store_add_list_show_export(tmp_path):
    artifact = tmp_path / "docs" / "report.md"
    artifact.parent.mkdir()
    artifact.write_text("# Report\n", encoding="utf-8")

    store = ArtifactStore(tmp_path)
    item = store.add("docs/report.md", label="Report", kind="doc", description="Operator report", tags=("release", "audit"))

    assert item["path"] == "docs/report.md"
    assert item["label"] == "Report"
    assert item["kind"] == "doc"
    assert item["sha256"] == sha256_file(artifact)
    assert item["tags"] == ["release", "audit"]
    assert store.get(item["id"])["size_bytes"] == artifact.stat().st_size
    assert store.list(kind="doc")[0]["id"] == item["id"]

    exported = store.export_json()
    assert exported["schema_version"]["version"] == 1
    assert exported["artifacts"][0]["path"] == "docs/report.md"


def test_artifact_store_blocks_unsafe_paths(tmp_path):
    secret = tmp_path / ".env"
    secret.write_text("TOKEN=x", encoding="utf-8")

    store = ArtifactStore(tmp_path)
    try:
        store.add(".env")
    except ValueError as exc:
        assert "secret" in str(exc).lower() or ".env" in str(exc).lower()
    else:
        raise AssertionError("expected unsafe artifact path to be blocked")


def test_artifact_cli_commands(tmp_path, monkeypatch, capsys):
    artifact = tmp_path / "result.txt"
    artifact.write_text("ok", encoding="utf-8")
    monkeypatch.setattr("zai_coder.config.load_config", lambda path=None: ZaiConfig(workspace=str(tmp_path)))
    parser = build_parser()

    ns = parser.parse_args(["artifact", "add", "--path", "result.txt", "--label", "Result", "--kind", "report", "--tags", "ci,local"])
    assert ns.func(ns) == 0
    created = json.loads(capsys.readouterr().out)
    assert created["label"] == "Result"

    ns = parser.parse_args(["artifact", "list"])
    assert ns.func(ns) == 0
    listed = json.loads(capsys.readouterr().out)
    assert listed[0]["id"] == created["id"]

    ns = parser.parse_args(["artifact", "export", "--json"])
    assert ns.func(ns) == 0
    exported = json.loads(capsys.readouterr().out)
    assert exported["artifacts"][0]["sha256"] == created["sha256"]

