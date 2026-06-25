"""Enterprise admin console control helpers."""

from __future__ import annotations

from .directory import tenant_directory, workspace_directory, user_directory, directory_validation_report, invite_user_plan
from .rbac import role_matrix, admin_permission_decision, role_assignment_policy
from .feature_flags import feature_flag_catalog, feature_flag_validation_report, feature_flag_change_plan
from .config_registry import config_registry, config_validation_report, config_change_plan
from .service_control import service_catalog, service_action_plan, service_action_gate
from .support_access import support_access_policy, support_access_gate
from .audit_explorer import unified_audit_preview
from .exporter import write_admin_export
from .audit import AdminAuditLog


def admin_console_status() -> dict:
    return {
        "ok": True,
        "systems": [
            "admin_dashboard",
            "tenant_directory",
            "workspace_directory",
            "user_directory",
            "rbac_editor",
            "feature_flags",
            "config_registry",
            "service_control_panel",
            "audit_explorer",
            "support_access_guard",
            "admin_export_tools",
        ],
    }


def admin_overview() -> dict:
    return {
        "status": admin_console_status(),
        "tenants": tenant_directory(),
        "workspaces": workspace_directory(),
        "users": user_directory(),
        "directory_validation": directory_validation_report(),
        "roles": role_matrix(),
        "flags": feature_flag_catalog(),
        "flag_validation": feature_flag_validation_report(),
        "config": config_registry(),
        "config_validation": config_validation_report(),
        "services": service_catalog(),
    }


def admin_action_demo(root: str = ".") -> dict:
    invite = invite_user_plan("new.user@example.local", "New User", "org_local", "ws_default")
    flag = feature_flag_change_plan("self-healing", True, "ws_default", "approved_manual_001")
    svc_plan = service_action_plan("gateway", "healthcheck")
    svc_gate = service_action_gate(svc_plan.to_dict(), approval_id="approved_manual_001")
    support = support_access_gate(("support_agent",), user_directory("org_demo")[0], "approved_support_001", 15)
    export_path = write_admin_export(root)
    audit = AdminAuditLog().record("system", "admin.demo_planned", "admin-console", {"invite": invite, "flag": flag})
    return {
        "invite": invite,
        "feature_flag": flag,
        "service_plan": svc_plan.to_dict(),
        "service_gate": svc_gate,
        "support_access": support,
        "export_path": export_path,
        "audit": audit.to_dict(),
    }
