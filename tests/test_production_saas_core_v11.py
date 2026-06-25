import tempfile
from pathlib import Path

from zai_coder.production_saas_core.models import Organization, Workspace, UserAccount, Invitation
from zai_coder.production_saas_core.store import SaasStore
from zai_coder.production_saas_core.permissions import has_permission
from zai_coder.production_saas_core.auth_enforcement import enforce_api_key
from zai_coder.production_saas_core.quota_enforcement import check_quota
from zai_coder.production_saas_core.dashboards import render_billing_dashboard, render_usage_dashboard, render_audit_dashboard, render_settings_dashboard
from zai_coder.production_saas_core.integration_audit import IntegrationAuditLog
from zai_coder.production_saas_core.job_retry import RetryPolicy
from zai_coder.production_saas_core.cli.migrations_cli import migrations_command
from zai_coder.production_saas_core.cli.worker_daemon import worker_run_once
from zai_coder.production_saas_core.wizards.first_run import build_first_run_plan
from zai_coder.production_saas_core.wizards.deployment import build_deployment_plan
from zai_coder.production_saas_core.routes import (
    route_saas_status,
    route_billing_dashboard,
    route_usage_dashboard,
    route_audit_dashboard,
    route_settings_dashboard,
    route_first_run_plan,
    route_deployment_plan,
)
from zai_coder.monetization_core.usage import UsageStore


def test_models_validate():
    assert UserAccount("u1", "a@example.com", "A").validate() == []
    assert Organization("o1", "org", "Org", "u1").validate() == []
    assert Workspace("w1", "o1", "main", "Main").validate() == []
    assert Invitation("i1", "o1", "b@example.com", "developer", "u1").validate() == []


def test_saas_store_create_core_entities():
    with tempfile.TemporaryDirectory() as td:
        store = SaasStore(Path(td) / "saas.db")
        user = store.create_user("admin@example.com", "Admin")
        org = store.create_organization("zeaz", "ZEAZ", user.id, "builder")
        ws = store.create_workspace(org.id, "main", "Main")
        inv = store.create_invitation(org.id, "dev@example.com", "developer", user.id)
        assert store.count_members(org.id) == 1
        assert store.count_workspaces(org.id) == 1
        assert store.list_organizations()[0].slug == "zeaz"
        assert inv.role == "developer"


def test_permissions_and_auth_enforcement():
    assert has_permission(["owner"], "billing:write")
    assert has_permission(["admin"], "workspace:write")
    assert not has_permission(["viewer"], "billing:write")

    class Rec:
        name = "admin-key"

    allowed = enforce_api_key(Rec(), "workspace:write", ["admin"])
    denied = enforce_api_key(None, "workspace:write", ["admin"])
    assert allowed.allowed is True
    assert denied.allowed is False


def test_quota_enforcement():
    with tempfile.TemporaryDirectory() as td:
        usage = UsageStore(Path(td) / "usage.db")
        usage.record("acct", "ws", "agent_run", 1, "test")
        decision = check_quota(usage, "acct", "free", "agent_run", 1)
        assert decision.allowed is True
        assert decision.limit >= 50


def test_dashboards_render():
    assert "Billing Dashboard" in render_billing_dashboard([{"slug":"free","name":"Free","monthly_price_cents":0,"max_members":1}], [])
    assert "Usage Dashboard" in render_usage_dashboard([{"resource":"agent_run","units":1,"source":"test"}], [])
    assert "Audit Dashboard" in render_audit_dashboard([{"actor":"system","action":"x","target":"y","created_at":"now"}])
    assert "Admin Settings" in render_settings_dashboard({"mode":"local"})


def test_integration_audit_log():
    with tempfile.TemporaryDirectory() as td:
        audit = IntegrationAuditLog(Path(td) / "audit.db")
        event = audit.record("github", "status", "tester", {"ok": True})
        assert event.provider == "github"
        assert event.dry_run is True


def test_retry_policy():
    policy = RetryPolicy(max_attempts=3, base_delay_seconds=5)
    assert policy.delay_for_attempt(1) == 5
    assert policy.delay_for_attempt(2) == 10
    assert policy.should_retry(1, "failed")
    assert not policy.should_retry(3, "failed")


def test_cli_facades_and_wizards():
    with tempfile.TemporaryDirectory() as td:
        assert migrations_command(Path(td) / "app.db", apply=False)["migrations"]
        assert worker_run_once(Path(td) / "worker.db")["ran"] is False
    assert build_first_run_plan("admin@example.com").dry_run is True
    assert build_deployment_plan("zai.zeaz.dev").dry_run is True


def test_routes():
    assert route_saas_status()["ok"] is True
    assert route_billing_dashboard()["content_type"] == "text/html"
    assert route_usage_dashboard()["content_type"] == "text/html"
    assert route_audit_dashboard()["content_type"] == "text/html"
    assert route_settings_dashboard()["content_type"] == "text/html"
    assert route_first_run_plan({"admin_email":"admin@example.com"})["dry_run"] is True
    assert route_deployment_plan({"hostname":"zai.zeaz.dev"})["dry_run"] is True


def test_scripts_docs_exist():
    root = Path(__file__).resolve().parents[1]
    assert (root / "scripts/saas/first-run-plan.sh").exists()
    assert (root / "docs/requirements/NEXT_V11_PRODUCTION_SAAS_CORE_REQUIREMENTS.md").exists()
    assert (root / "docs/requirements/NEXT_REQUIREMENTS_V12_APP_STUDIO_FINAL.md").exists()
