"""Enterprise admin RBAC."""

from __future__ import annotations

ROLE_PERMISSIONS = {
    "super_admin": {"admin:*"},
    "tenant_admin": {"admin:view", "admin:user", "admin:workspace", "admin:feature", "admin:audit", "support:approve"},
    "ops_admin": {"admin:view", "admin:service", "admin:audit", "ops:plan"},
    "billing_admin": {"admin:view", "billing:view", "billing:manage"},
    "compliance_admin": {"admin:view", "compliance:view", "compliance:report", "admin:audit"},
    "support_agent": {"admin:view", "support:view"},
    "viewer": {"admin:view"},
}


def permissions_for_roles(roles: tuple[str, ...] | list[str]) -> set[str]:
    permissions = set()
    for role in roles:
        permissions.update(ROLE_PERMISSIONS.get(role, set()))
    return permissions


def admin_permission_decision(roles: tuple[str, ...] | list[str], required: str) -> dict:
    permissions = permissions_for_roles(tuple(roles))
    domain = required.split(":", 1)[0]
    allowed = required in permissions or "admin:*" in permissions or f"{domain}:*" in permissions
    return {"allowed": allowed, "required": required, "roles": list(roles), "permissions": sorted(permissions)}


def role_matrix() -> dict:
    return {role: sorted(perms) for role, perms in ROLE_PERMISSIONS.items()}


def role_assignment_policy(actor_roles: tuple[str, ...], target_roles: tuple[str, ...]) -> dict:
    actor = permissions_for_roles(actor_roles)
    blocked = []
    if "admin:*" not in actor and "super_admin" in target_roles:
        blocked.append("only super_admin may assign super_admin")
    if "admin:user" not in actor and "admin:*" not in actor:
        blocked.append("actor lacks admin:user")
    return {"allowed": not blocked, "blocked": blocked, "actor_roles": list(actor_roles), "target_roles": list(target_roles)}
