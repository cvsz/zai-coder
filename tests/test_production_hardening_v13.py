import tempfile
from pathlib import Path

import pytest

from zai_coder.production_hardening_core.server.app_factory import AppSettings, build_route_manifest
from zai_coder.production_hardening_core.server.health import health_payload, readiness_payload
from zai_coder.production_hardening_core.auth.session_store import SessionStore
from zai_coder.production_hardening_core.auth.middleware import require_session_header
from zai_coder.production_hardening_core.db.postgres_adapter import PostgresSettings, PostgresAdapter
from zai_coder.production_hardening_core.migrations.manager import RevisionManager
from zai_coder.production_hardening_core.ops.backup_policy import default_backup_policy
from zai_coder.production_hardening_core.ops.smoke_tests import production_smoke_test_plan


def test_app_settings_and_routes():
    settings = AppSettings()
    assert settings.environment == "production"
    routes = build_route_manifest()
    assert any(route["path"] == "/healthz" for route in routes)
    assert any(route["auth"] is True for route in routes)


def test_health_and_readiness():
    with tempfile.TemporaryDirectory() as td:
        settings = {"environment": "production", "session_db_path": str(Path(td) / "sessions.db")}
        assert health_payload(settings)["ok"] is True
        assert readiness_payload(settings)["ok"] is True


def test_session_store_create_verify_revoke():
    with tempfile.TemporaryDirectory() as td:
        store = SessionStore(Path(td) / "sessions.db")
        session = store.create_session("admin", scopes=("admin",))
        verified = store.verify_session(session.token)
        assert verified is not None
        assert verified.actor == "admin"
        decision = require_session_header(store, session.token)
        assert decision.allowed is True
        store.revoke_session(session.token)
        assert store.verify_session(session.token) is None


def test_postgres_settings_validation_and_safe_dict():
    good = PostgresSettings("postgresql://user@localhost:5432/zai")
    assert good.validate() == []
    safe = good.safe_dict()
    assert safe["host"] == "localhost"
    assert safe["database"] == "zai"
    adapter = PostgresAdapter(good)
    assert adapter.connection_kwargs()["safe"]["database"] == "zai"

    bad = PostgresSettings("sqlite:///tmp.db")
    assert bad.validate()


def test_revision_manager_dry_run_and_apply():
    with tempfile.TemporaryDirectory() as td:
        mgr = RevisionManager(Path(td) / "prod.db")
        plan = mgr.upgrade(apply=False)
        assert plan and plan[0]["dry_run"] is True
        applied = mgr.upgrade(apply=True)
        assert applied and applied[0]["dry_run"] is False
        assert mgr.plan() == []


def test_backup_policy_and_smoke_plan():
    policy = default_backup_policy()
    assert policy.validate() == []
    assert policy.encryption_required is True
    plan = production_smoke_test_plan("http://127.0.0.1:8765")
    assert plan["dry_run"] is True
    assert len(plan["checks"]) >= 4


def test_production_files_exist():
    root = Path(__file__).resolve().parents[1]
    for rel in [
        "requirements-production.txt",
        "Dockerfile.production",
        "deploy/docker/docker-compose.production-hardening.yml",
        "deploy/systemd/zai-coder-production-hardening.service",
        "deploy/cloudflare/cloudflare-access-production.md",
        "docs/production/PRODUCTION_HARDENING_GUIDE.md",
        "docs/production/MONITORING_LOGGING.md",
        "docs/production/BACKUP_POLICY.md",
        "docs/production/PRODUCTION_SMOKE_TESTS.md",
        "scripts/production/serve-fastapi.sh",
        "scripts/production/migrate-production.sh",
    ]:
        assert (root / rel).exists(), rel
