"""Tenant-scoped connector permissions."""

from __future__ import annotations

ROLE_CONNECTOR_PERMISSIONS = {
    "tenant_owner": {"connector:*"},
    "tenant_admin": {"connector:view", "connector:install", "connector:enable", "connector:disable", "github:read", "drive:read", "slack:read", "providers:plan"},
    "operator": {"connector:view", "connector:install", "github:read", "providers:plan"},
    "analyst": {"connector:view", "drive:read", "slack:read"},
    "viewer": {"connector:view"},
}


def permissions_for_roles(roles: tuple[str, ...]) -> set[str]:
    permissions = set()
    for role in roles:
        permissions.update(ROLE_CONNECTOR_PERMISSIONS.get(role, set()))
    return permissions


def connector_permission_decision(roles: tuple[str, ...], required_permissions: tuple[str, ...]) -> dict:
    permissions = permissions_for_roles(roles)
    missing = []
    for required in required_permissions:
        domain = required.split(":", 1)[0]
        if required not in permissions and "connector:*" not in permissions and f"{domain}:*" not in permissions:
            missing.append(required)
    return {"allowed": not missing, "roles": list(roles), "permissions": sorted(permissions), "missing": missing}
