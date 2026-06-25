from pathlib import Path
import tempfile

from zai_coder.multi_tenant_control.models import TenantOrg, Workspace, TenantPrincipal, WorkspaceQuota
from zai_coder.multi_tenant_control.store import TenantStore
from zai_coder.multi_tenant_control.api_keys import TenantApiKeyStore
from zai_coder.multi_tenant_control.isolation import cross_tenant_access_guard, has_tenant_permission
from zai_coder.multi_tenant_control.quotas import quota_decision, default_usage
from zai_coder.multi_tenant_control.audit import build_tenant_audit_event, audit_scope_filter
from zai_coder.multi_tenant_control.provider_permissions import provider_permission_decision
from zai_coder.multi_tenant_control.backup_export import tenant_backup_policy, tenant_export_path, write_tenant_export
from zai_coder.multi_tenant_control.onboarding import tenant_onboarding_plan
from zai_coder.multi_tenant_control.migration import tenant_migration_plan
from zai_coder.multi_tenant_control.ui.pages import render_tenant_overview, render_onboarding_page, render_backup_page, render_migration_page
from zai_coder.multi_tenant_control.routes import (
    route_tenant_status,
    route_tenant_onboarding_plan,
    route_tenant_backup_policy,
    route_tenant_migration_plan,
    route_tenant_isolation_check,
    route_quota_decision,
    route_provider_permission,
    route_create_tenant_demo,
    route_create_tenant_api_key,
    route_tenant_page,
    route_tenant_onboarding_page,
    route_tenant_backup_page,
    route_tenant_migration_page,
)


def test_models_validation():
    assert TenantOrg("org1", "Org", "org").validate() == []
    assert TenantOrg("", "", "../bad").validate()
    assert Workspace("ws1", "org1", "Default", "default").validate() == []
    assert Workspace("", "", "", "../x").validate()
    assert WorkspaceQuota("org1", "ws1").validate() == []


def test_store_org_workspace_membership_audit_quota():
    with tempfile.TemporaryDirectory() as td:
        store = TenantStore(Path(td) / "tenants.db")
        org = store.create_org("Local Org", "local-org")
        ws = store.create_workspace(org.id, "Default", "default")
        principal = TenantPrincipal("admin", org.id, ws.id, ("tenant_owner",))
        store.add_membership(principal)
        assert store.get_membership("admin", org.id, ws.id).roles == ("tenant_owner",)
        event = store.record_audit(build_tenant_audit_event(principal, "test.action", ws.id))
        events = store.list_audit(org.id, ws.id)
        assert events[0]["id"] == event.id
        assert store.get_quota(org.id, ws.id).monthly_runs_limit == 1000


def test_api_keys_scope_and_hashing():
    with tempfile.TemporaryDirectory() as td:
        key_store = TenantApiKeyStore(Path(td) / "keys.db")
        key, token = key_store.create_key("org1", "ws1", "demo", ("workspace:view",))
        assert key.token_prefix in token
        assert key_store.verify_key(token, "org1", "ws1")["allowed"] is True
        assert key_store.verify_key(token, "org2", "ws1")["allowed"] is False
        assert key_store.verify_key(token, "org1", "ws1", "providers:apply")["allowed"] is False


def test_isolation_quota_audit_provider_permissions():
    principal = TenantPrincipal("admin", "org1", "ws1", ("tenant_admin",))
    assert has_tenant_permission(principal, "providers:apply")
    assert cross_tenant_access_guard(principal, "org1", "ws2")["allowed"] is True
    assert cross_tenant_access_guard(principal, "org2", "ws1")["allowed"] is False
    operator = TenantPrincipal("op", "org1", "ws1", ("operator",))
    assert cross_tenant_access_guard(operator, "org1", "ws2")["allowed"] is False
    quota = WorkspaceQuota("org1", "ws1", monthly_runs_limit=1, storage_mb_limit=10, provider_apply_limit=1)
    assert quota_decision(quota, {"monthly_runs": 1, "storage_mb": 10, "provider_apply": 1})["allowed"] is True
    assert quota_decision(quota, {"monthly_runs": 2})["allowed"] is False
    event = build_tenant_audit_event(principal, "action", "target")
    assert audit_scope_filter([event.to_dict()], "org1", "ws1")
    assert provider_permission_decision(principal, "github", False)["allowed"] is True
    assert provider_permission_decision(operator, "docker", True)["allowed"] is False


def test_backup_export_onboarding_migration(tmp_path):
    assert tenant_export_path("org", "ws") == "exports/tenants/org/ws/export.json"
    assert tenant_backup_policy()["dry_run"] is True
    out = write_tenant_export({"ok": True}, "org", "ws", tmp_path)
    assert Path(out).exists()
    assert tenant_onboarding_plan()["dry_run"] is True
    migration = tenant_migration_plan()
    assert migration["dry_run"] is True
    assert "verify tenant isolation checks" in migration["steps"]


def test_ui_pages():
    assert "Multi-Tenant Control" in render_tenant_overview()
    assert "Tenant Onboarding" in render_onboarding_page()
    assert "Tenant Backup" in render_backup_page()
    assert "Tenant Migration" in render_migration_page()


def test_routes(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert route_tenant_status()["ok"] is True
    assert route_tenant_onboarding_plan()["dry_run"] is True
    assert route_tenant_backup_policy()["dry_run"] is True
    assert route_tenant_migration_plan()["dry_run"] is True
    assert route_tenant_isolation_check()["allowed"] is True
    assert route_tenant_isolation_check({"org_id":"a","workspace_id":"w","target_org_id":"b","target_workspace_id":"w"})["allowed"] is False
    assert route_quota_decision({"usage": default_usage()})["allowed"] is True
    assert route_provider_permission({"provider":"github"})["allowed"] is True
    demo = route_create_tenant_demo()
    assert demo["org"]["id"].startswith("org_")
    key = route_create_tenant_api_key()
    assert "token_preview" in key
    assert route_tenant_page()["content_type"] == "text/html"
    assert route_tenant_onboarding_page()["content_type"] == "text/html"
    assert route_tenant_backup_page()["content_type"] == "text/html"
    assert route_tenant_migration_page()["content_type"] == "text/html"


def test_docs_scripts_assets_exist():
    root = Path(__file__).resolve().parents[1]
    for rel in [
        "scripts/tenants/tenant-status.sh",
        "scripts/tenants/tenant-onboarding-plan.sh",
        "scripts/tenants/tenant-demo-create.sh",
        "scripts/tenants/tenant-api-key-plan.sh",
        "scripts/tenants/tenant-isolation-check.sh",
        "scripts/tenants/workspace-quota-check.sh",
        "scripts/tenants/tenant-provider-permission.sh",
        "scripts/tenants/tenant-backup-policy.sh",
        "scripts/tenants/tenant-migration-plan.sh",
        "scripts/tenants/tenant-dashboard-export.sh",
        "docs/tenants/MULTI_TENANT_CONTROL_GUIDE.md",
        "docs/tenants/TENANT_ISOLATION_POLICY.md",
        "docs/tenants/TENANT_API_KEYS.md",
        "docs/tenants/WORKSPACE_QUOTAS.md",
        "docs/tenants/TENANT_BACKUP_EXPORT.md",
        "docs/tenants/TENANT_MIGRATION_PLAN.md",
        "docs/requirements/NEXT_V21_MULTI_TENANT_CONTROL_REQUIREMENTS.md",
        "assets/tenants/multi_tenant_control_features.json",
    ]:
        assert (root / rel).exists(), rel
