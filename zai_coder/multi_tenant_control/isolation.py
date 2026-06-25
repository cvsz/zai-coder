"""Cross-tenant access guard."""

from __future__ import annotations

from .models import TenantPrincipal


TENANT_ROLE_PERMISSIONS = {
    "tenant_owner": {"tenant:*"},
    "tenant_admin": {"tenant:view", "tenant:write", "workspace:view", "workspace:write", "providers:plan", "providers:apply"},
    "workspace_admin": {"workspace:view", "workspace:write", "providers:plan", "providers:apply"},
    "operator": {"workspace:view", "providers:plan"},
    "viewer": {"workspace:view"},
}


def tenant_permissions(roles: tuple[str, ...]) -> set[str]:
    permissions: set[str] = set()
    for role in roles:
        permissions.update(TENANT_ROLE_PERMISSIONS.get(role, set()))
    return permissions


def has_tenant_permission(principal: TenantPrincipal, permission: str) -> bool:
    permissions = tenant_permissions(principal.roles)
    if "tenant:*" in permissions or permission in permissions:
        return True
    domain = permission.split(":", 1)[0]
    return f"{domain}:*" in permissions


def cross_tenant_access_guard(principal: TenantPrincipal, target_org_id: str, target_workspace_id: str, permission: str = "workspace:view") -> dict:
    if principal.org_id != target_org_id:
        return {"allowed": False, "reason": "cross-org access denied"}
    if principal.workspace_id != target_workspace_id and "tenant_owner" not in principal.roles and "tenant_admin" not in principal.roles:
        return {"allowed": False, "reason": "cross-workspace access denied"}
    if not has_tenant_permission(principal, permission):
        return {"allowed": False, "reason": f"missing permission: {permission}"}
    return {"allowed": True, "reason": "allowed"}
