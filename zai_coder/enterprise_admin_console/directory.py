"""Admin directory for tenants, workspaces, and users."""

from __future__ import annotations

import uuid

from .models import AdminTenant, AdminWorkspace, AdminUser


DEFAULT_TENANTS = [
    AdminTenant("org_local", "Local Organization", "internal", "active", "global"),
    AdminTenant("org_demo", "Demo Customer", "free", "trial", "global"),
]

DEFAULT_WORKSPACES = [
    AdminWorkspace("ws_default", "org_local", "Default Workspace", "active", "internal"),
    AdminWorkspace("ws_demo", "org_demo", "Demo Workspace", "active", "default"),
]

DEFAULT_USERS = [
    AdminUser("usr_admin", "admin@example.local", "Admin User", ("tenant_admin", "ops_admin"), "active", "org_local", "ws_default"),
    AdminUser("usr_viewer", "viewer@example.local", "Viewer User", ("viewer",), "active", "org_local", "ws_default"),
    AdminUser("usr_support", "support@example.local", "Support User", ("support_agent",), "active", "org_demo", "ws_demo"),
]


def tenant_directory() -> list[dict]:
    return [tenant.to_dict() for tenant in DEFAULT_TENANTS]


def workspace_directory(org_id: str | None = None) -> list[dict]:
    rows = DEFAULT_WORKSPACES
    if org_id:
        rows = [row for row in rows if row.org_id == org_id]
    return [workspace.to_dict() for workspace in rows]


def user_directory(org_id: str | None = None, workspace_id: str | None = None) -> list[dict]:
    rows = DEFAULT_USERS
    if org_id:
        rows = [row for row in rows if row.org_id == org_id]
    if workspace_id:
        rows = [row for row in rows if row.workspace_id == workspace_id]
    return [user.to_dict() for user in rows]


def directory_validation_report() -> dict:
    reports = []
    for item in [*DEFAULT_TENANTS, *DEFAULT_WORKSPACES, *DEFAULT_USERS]:
        reports.append({"id": item.id, "issues": item.validate()})
    return {"ok": all(not item["issues"] for item in reports), "reports": reports}


def invite_user_plan(email: str, display_name: str, org_id: str, workspace_id: str, roles: tuple[str, ...] = ("viewer",)) -> dict:
    user = AdminUser(f"usr_{uuid.uuid4().hex[:12]}", email, display_name, roles, "invited", org_id, workspace_id)
    issues = user.validate()
    return {"dry_run": True, "allowed": not issues, "issues": issues, "user": user.to_dict(), "send_email": False}
