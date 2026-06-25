"""Tenant-scoped skill permissions."""

from __future__ import annotations

ROLE_SKILL_PERMISSIONS = {
    "tenant_owner": {"skill:*"},
    "tenant_admin": {"skill:view", "skill:install", "skill:enable", "skill:disable", "release:check", "providers:plan", "billing:view"},
    "operator": {"skill:view", "skill:install", "skill:enable", "release:check", "providers:plan"},
    "analyst": {"skill:view", "billing:view"},
    "viewer": {"skill:view"},
}


def permissions_for_roles(roles: tuple[str, ...]) -> set[str]:
    permissions = set()
    for role in roles:
        permissions.update(ROLE_SKILL_PERMISSIONS.get(role, set()))
    return permissions


def skill_permission_decision(roles: tuple[str, ...], required_permissions: tuple[str, ...]) -> dict:
    permissions = permissions_for_roles(roles)
    missing = []
    for required in required_permissions:
        domain = required.split(":", 1)[0]
        if required not in permissions and "skill:*" not in permissions and f"{domain}:*" not in permissions:
            missing.append(required)
    return {"allowed": not missing, "roles": list(roles), "permissions": sorted(permissions), "missing": missing}
