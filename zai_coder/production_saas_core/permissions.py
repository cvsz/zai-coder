"""SaaS role and permission policy."""

from __future__ import annotations

from typing import Iterable, Set


ROLE_PERMISSIONS = {
    "owner": {"*:*"},
    "admin": {"org:read", "org:write", "workspace:*", "members:*", "billing:read", "usage:read", "audit:read"},
    "developer": {"org:read", "workspace:read", "agent:run", "runs:read", "integrations:plan", "usage:read"},
    "marketer": {"org:read", "workspace:read", "creative:*", "social:*", "integrations:plan"},
    "billing": {"org:read", "billing:*", "usage:read", "audit:read"},
    "viewer": {"org:read", "workspace:read", "runs:read", "audit:read"},
}


def normalize_role(role: str) -> str:
    role = (role or "").strip().lower()
    if role not in ROLE_PERMISSIONS:
        raise ValueError(f"unknown role: {role}")
    return role


def permissions_for_roles(roles: Iterable[str]) -> Set[str]:
    permissions: Set[str] = set()
    for role in roles:
        permissions.update(ROLE_PERMISSIONS[normalize_role(role)])
    return permissions


def has_permission(roles: Iterable[str], permission: str) -> bool:
    permission = permission.strip().lower()
    perms = permissions_for_roles(roles)
    if "*:*" in perms or permission in perms:
        return True
    prefix = permission.split(":", 1)[0]
    return f"{prefix}:*" in perms
