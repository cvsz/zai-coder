from pathlib import Path

from zai_coder.enterprise_admin_console.models import AdminUser, AdminTenant, AdminWorkspace, FeatureFlag, ConfigEntry, ServiceActionPlan
from zai_coder.enterprise_admin_console.rbac import permissions_for_roles, admin_permission_decision, role_matrix, role_assignment_policy
from zai_coder.enterprise_admin_console.directory import tenant_directory, workspace_directory, user_directory, directory_validation_report, invite_user_plan
from zai_coder.enterprise_admin_console.feature_flags import feature_flag_catalog, feature_flag_validation_report, feature_flag_change_plan
from zai_coder.enterprise_admin_console.config_registry import config_registry, config_validation_report, config_change_plan
from zai_coder.enterprise_admin_console.service_control import service_catalog, service_action_plan, service_action_gate
from zai_coder.enterprise_admin_console.support_access import support_access_policy, support_access_gate
from zai_coder.enterprise_admin_console.audit_explorer import audit_sources, audit_query_plan, unified_audit_preview
from zai_coder.enterprise_admin_console.exporter import admin_export_bundle, write_admin_export
from zai_coder.enterprise_admin_console.audit import AdminAuditLog
from zai_coder.enterprise_admin_console.control import admin_console_status, admin_overview, admin_action_demo
from zai_coder.enterprise_admin_console.ui.pages import render_admin_overview_page, render_tenants_page, render_users_page, render_flags_page, render_services_page
from zai_coder.enterprise_admin_console.routes import (
    route_admin_status,
    route_admin_overview,
    route_admin_directory,
    route_admin_invite_plan,
    route_admin_rbac,
    route_admin_feature_flags,
    route_admin_config,
    route_admin_services,
    route_admin_support_access,
    route_admin_audit_explorer,
    route_admin_export,
    route_admin_action_demo,
    route_admin_audit,
    route_admin_page,
    route_admin_tenants_page,
    route_admin_users_page,
    route_admin_flags_page,
    route_admin_services_page,
)


def test_models_validation():
    assert AdminUser("u", "u@example.local", "User").validate() == []
    assert AdminUser("", "bad", "", status="bad").validate()
    assert AdminTenant("o", "Org").validate() == []
    assert AdminTenant("", "", plan="bad", status="bad").validate()
    assert AdminWorkspace("w", "o", "Workspace").validate() == []
    assert AdminWorkspace("", "", "", status="bad").validate()
    assert FeatureFlag("f", "Flag").validate() == []
    assert FeatureFlag("../bad", "", scope="bad").validate()
    assert ConfigEntry("key", "value").validate() == []
    assert ConfigEntry("secret", "value", secret=True).validate()
    assert ServiceActionPlan("p", "gateway", "status", ("make healthcheck",)).validate() == []


def test_rbac_directory_flags_config_services():
    assert "admin:view" in permissions_for_roles(("viewer",))
    assert admin_permission_decision(("viewer",), "admin:view")["allowed"] is True
    assert role_matrix()["viewer"]
    assert role_assignment_policy(("tenant_admin",), ("viewer",))["allowed"] is True
    assert role_assignment_policy(("viewer",), ("super_admin",))["allowed"] is False
    assert tenant_directory()
    assert workspace_directory("org_local")
    assert user_directory("org_local", "ws_default")
    assert directory_validation_report()["ok"] is True
    assert invite_user_plan("new@example.local", "New", "org_local", "ws_default")["allowed"] is True
    assert feature_flag_catalog()
    assert feature_flag_validation_report()["ok"] is True
    assert feature_flag_change_plan("self-healing", True, "ws_default", "approved_manual_001")["allowed"] is True
    assert feature_flag_change_plan("gateway-v2", False)["allowed"] is False
    assert config_registry()
    assert config_validation_report()["ok"] is True
    assert config_change_plan("app.mode", "enterprise")["allowed"] is True
    assert config_change_plan("providers.github.token", "x")["allowed"] is False
    assert service_catalog()
    plan = service_action_plan("gateway", "healthcheck")
    assert plan.dry_run is True
    assert service_action_gate(plan.to_dict())["allowed"] is True
    restart = service_action_plan("gateway", "restart-plan")
    assert service_action_gate(restart.to_dict())["allowed"] is False


def test_support_audit_export_control(tmp_path):
    target = user_directory("org_demo")[0]
    assert support_access_policy()["requires_customer_approval"] is True
    assert support_access_gate(("support_agent",), target, "approved_support_001", 15)["allowed"] is True
    assert support_access_gate(("viewer",), target, "", 90)["allowed"] is False
    assert audit_sources()
    assert audit_query_plan("admin", 10)["dry_run"] is True
    assert unified_audit_preview()["sources"]
    bundle = admin_export_bundle()
    assert bundle["secrets_redacted"] is True
    path = write_admin_export(tmp_path)
    assert Path(path).exists()
    audit = AdminAuditLog(tmp_path / "admin.db")
    event = audit.record("tester", "admin.test", "target")
    assert audit.list_events()[0]["id"] == event.id
    assert admin_console_status()["ok"] is True
    assert admin_overview()["status"]["ok"] is True
    demo = admin_action_demo(str(tmp_path))
    assert Path(demo["export_path"]).exists()


def test_ui_routes(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert "Enterprise Admin Console" in render_admin_overview_page()
    assert "Tenants" in render_tenants_page()
    assert "Users" in render_users_page()
    assert "Feature Flags" in render_flags_page()
    assert "Services" in render_services_page()
    assert route_admin_status()["ok"] is True
    assert route_admin_overview()["status"]["ok"] is True
    assert route_admin_directory()["validation"]["ok"] is True
    assert route_admin_invite_plan()["allowed"] is True
    assert route_admin_rbac()["view_gate"]["allowed"] is True
    assert route_admin_feature_flags()["validation"]["ok"] is True
    assert route_admin_config()["validation"]["ok"] is True
    assert route_admin_services()["gate"]["allowed"] is True
    assert route_admin_support_access()["gate"]["allowed"] is True
    assert route_admin_audit_explorer()["sources"]
    assert Path(route_admin_export()["path"]).exists()
    assert Path(route_admin_action_demo()["export_path"]).exists()
    assert "events" in route_admin_audit()
    assert route_admin_page()["content_type"] == "text/html"
    assert route_admin_tenants_page()["content_type"] == "text/html"
    assert route_admin_users_page()["content_type"] == "text/html"
    assert route_admin_flags_page()["content_type"] == "text/html"
    assert route_admin_services_page()["content_type"] == "text/html"


def test_docs_scripts_assets_exist():
    root = Path(__file__).resolve().parents[1]
    for rel in [
        "scripts/admin-console/admin-status.sh",
        "scripts/admin-console/admin-directory.sh",
        "scripts/admin-console/admin-invite-plan.sh",
        "scripts/admin-console/admin-rbac.sh",
        "scripts/admin-console/admin-feature-flags.sh",
        "scripts/admin-console/admin-config.sh",
        "scripts/admin-console/admin-services.sh",
        "scripts/admin-console/admin-support-access.sh",
        "scripts/admin-console/admin-audit-explorer.sh",
        "scripts/admin-console/admin-export.sh",
        "scripts/admin-console/admin-action-demo.sh",
        "scripts/admin-console/admin-audit.sh",
        "scripts/admin-console/admin-dashboard-export.sh",
        "docs/admin-console/ENTERPRISE_ADMIN_CONSOLE_GUIDE.md",
        "docs/admin-console/RBAC_ADMIN.md",
        "docs/admin-console/FEATURE_FLAGS.md",
        "docs/admin-console/CONFIG_REGISTRY.md",
        "docs/admin-console/SERVICE_CONTROL_PANEL.md",
        "docs/admin-console/SUPPORT_ACCESS_GUARD.md",
        "docs/requirements/NEXT_V33_ENTERPRISE_ADMIN_CONSOLE_REQUIREMENTS.md",
        "assets/admin-console/enterprise_admin_console_features.json",
    ]:
        assert (root / rel).exists(), rel
