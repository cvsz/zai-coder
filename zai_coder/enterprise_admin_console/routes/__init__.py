"""Enterprise Admin Console route registry."""

from __future__ import annotations

from zai_coder.enterprise_admin_console.control import admin_console_status, admin_overview, admin_action_demo
from zai_coder.enterprise_admin_console.directory import tenant_directory, workspace_directory, user_directory, directory_validation_report, invite_user_plan
from zai_coder.enterprise_admin_console.rbac import role_matrix, admin_permission_decision, role_assignment_policy
from zai_coder.enterprise_admin_console.feature_flags import feature_flag_catalog, feature_flag_change_plan, feature_flag_validation_report
from zai_coder.enterprise_admin_console.config_registry import config_registry, config_change_plan, config_validation_report
from zai_coder.enterprise_admin_console.service_control import service_catalog, service_action_plan, service_action_gate
from zai_coder.enterprise_admin_console.support_access import support_access_policy, support_access_gate
from zai_coder.enterprise_admin_console.audit_explorer import unified_audit_preview
from zai_coder.enterprise_admin_console.exporter import admin_export_bundle, write_admin_export
from zai_coder.enterprise_admin_console.audit import AdminAuditLog
from zai_coder.enterprise_admin_console.ui.pages import render_admin_overview_page, render_tenants_page, render_users_page, render_flags_page, render_services_page


def route_admin_status() -> dict:
    return {
        "ok": True,
        "service": "zai-enterprise-admin-console",
        "systems": [
            "admin_dashboard",
            "tenant_org_workspace_user_management",
            "rbac_editor",
            "feature_flags",
            "config_registry",
            "service_control_panel",
            "audit_explorer",
            "support_access_guard",
            "admin_export_tools",
            "admin_audit_log",
        ],
    }


def route_admin_overview() -> dict:
    return admin_overview()


def route_admin_directory() -> dict:
    return {"tenants": tenant_directory(), "workspaces": workspace_directory(), "users": user_directory(), "validation": directory_validation_report()}


def route_admin_invite_plan() -> dict:
    return invite_user_plan("new.user@example.local", "New User", "org_local", "ws_default")


def route_admin_rbac() -> dict:
    return {
        "roles": role_matrix(),
        "view_gate": admin_permission_decision(("viewer",), "admin:view"),
        "assign_gate": role_assignment_policy(("tenant_admin",), ("viewer",)),
    }


def route_admin_feature_flags() -> dict:
    return {"flags": feature_flag_catalog(), "validation": feature_flag_validation_report(), "change": feature_flag_change_plan("self-healing", True, "ws_default", "approved_manual_001")}


def route_admin_config() -> dict:
    return {"config": config_registry(), "validation": config_validation_report(), "change": config_change_plan("app.mode", "enterprise", "")}


def route_admin_services() -> dict:
    plan = service_action_plan("gateway", "healthcheck")
    return {"services": service_catalog(), "plan": plan.to_dict(), "gate": service_action_gate(plan.to_dict())}


def route_admin_support_access() -> dict:
    return {"policy": support_access_policy(), "gate": support_access_gate(("support_agent",), user_directory("org_demo")[0], "approved_support_001", 15)}


def route_admin_audit_explorer() -> dict:
    return unified_audit_preview()


def route_admin_export() -> dict:
    return {"bundle": admin_export_bundle(), "path": write_admin_export(".")}


def route_admin_action_demo() -> dict:
    return admin_action_demo(".")


def route_admin_audit() -> dict:
    return {"events": AdminAuditLog().list_events()}


def route_admin_page() -> dict:
    return {"content_type": "text/html", "html": render_admin_overview_page()}


def route_admin_tenants_page() -> dict:
    return {"content_type": "text/html", "html": render_tenants_page()}


def route_admin_users_page() -> dict:
    return {"content_type": "text/html", "html": render_users_page()}


def route_admin_flags_page() -> dict:
    return {"content_type": "text/html", "html": render_flags_page()}


def route_admin_services_page() -> dict:
    return {"content_type": "text/html", "html": render_services_page()}
