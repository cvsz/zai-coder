import tempfile
from pathlib import Path

import pytest

from zai_coder.app_studio.api_auth import ApiKeyManager
from zai_coder.app_studio.migrations import MigrationManager
from zai_coder.app_studio.event_bus import EventBus
from zai_coder.app_studio.worker import WorkerQueue
from zai_coder.app_studio.streaming import RunStream
from zai_coder.app_studio.dashboard import render_app_studio_dashboard
from zai_coder.app_studio.routes import route_status, route_dashboard


def test_api_key_manager_create_verify_revoke():
    with tempfile.TemporaryDirectory() as td:
        manager = ApiKeyManager(Path(td) / "app.db")
        record, raw_key = manager.create_key("admin")
        assert raw_key.startswith("zai_")
        assert manager.verify_key(raw_key).id == record.id
        manager.revoke_key(record.id)
        assert manager.verify_key(raw_key) is None


def test_migration_manager_dry_run_and_apply():
    with tempfile.TemporaryDirectory() as td:
        mgr = MigrationManager(Path(td) / "app.db")
        plan = mgr.apply(apply=False)
        assert plan and plan[0]["dry_run"] is True
        applied = mgr.apply(apply=True)
        assert applied and applied[0]["dry_run"] is False
        assert mgr.plan() == []


def test_event_bus_publish_subscribe():
    bus = EventBus()
    seen = []
    bus.subscribe("run", lambda event: seen.append(event))
    event = bus.publish("run", {"ok": True})
    assert seen[0].id == event.id
    assert bus.recent()[0].topic == "run"


def test_worker_queue_run_one():
    with tempfile.TemporaryDirectory() as td:
        q = WorkerQueue(Path(td) / "worker.db")
        q.register_handler("echo", lambda payload: {"echo": payload})
        q.enqueue("echo", {"hello": "zai"})
        result = q.run_one()
        assert result.status == "completed"
        assert result.result["echo"]["hello"] == "zai"


def test_worker_queue_missing_handler_fails_safely():
    with tempfile.TemporaryDirectory() as td:
        q = WorkerQueue(Path(td) / "worker.db")
        q.enqueue("missing", {})
        result = q.run_one()
        assert result.status == "failed"


def test_run_stream_events():
    stream = RunStream()
    event = stream.emit("run1", "message", {"text": "hello"})
    assert "event: message" in event.to_sse()
    assert len(stream.for_run("run1")) == 1


def test_dashboard_and_routes():
    html = render_app_studio_dashboard(
        [{"slug": "demo", "title": "Demo", "project_type": "game", "status": "draft"}],
        [{"email": "a@example.com", "display_name": "A", "status": "active"}],
        [{"slug": "free", "name": "Free", "monthly_price_cents": 0}],
        [{"id": "r1", "run_type": "agent", "status": "ok"}],
        [{"actor": "system", "action": "test", "target": "dashboard"}],
    )
    assert "ZAI App Studio" in html
    assert route_status()["ok"] is True
    assert route_dashboard({"projects": [], "members": [], "plans": [], "runs": [], "audit_events": []})["content_type"] == "text/html"


def test_deploy_files_exist():
    root = Path(__file__).resolve().parents[1]
    assert (root / "Dockerfile").exists()
    assert (root / "docker-compose.yml").exists()
    assert (root / "deploy/systemd/zai-coder.service").exists()
    assert (root / "deploy/cloudflare/tunnel-checklist.md").exists()
