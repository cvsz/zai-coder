"""Role and permission model for ZAI Coder members system."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable, Set


ROLE_PERMISSIONS: Dict[str, Set[str]] = {
    "owner": {
        "workspace:*",
        "members:*",
        "billing:*",
        "updates:*",
        "agents:*",
        "marketing:*",
        "social:*",
        "audit:read",
    },
    "admin": {
        "workspace:read",
        "workspace:write",
        "members:read",
        "members:write",
        "updates:read",
        "updates:apply",
        "agents:run",
        "marketing:*",
        "social:*",
        "audit:read",
    },
    "developer": {
        "workspace:read",
        "agents:run",
        "patch:check",
        "patch:apply",
        "memory:read",
        "audit:read",
    },
    "marketer": {
        "workspace:read",
        "marketing:*",
        "social:*",
        "assets:read",
        "assets:write",
    },
    "viewer": {
        "workspace:read",
        "runs:read",
        "audit:read",
        "assets:read",
    },
}


def normalize_role(role: str) -> str:
    value = (role or "").strip().lower()
    if value not in ROLE_PERMISSIONS:
        raise ValueError(f"unknown role: {role}")
    return value


def permissions_for_roles(roles: Iterable[str]) -> Set[str]:
    permissions: Set[str] = set()
    for role in roles:
        permissions.update(ROLE_PERMISSIONS[normalize_role(role)])
    return permissions


def has_permission(roles: Iterable[str], permission: str) -> bool:
    permission = permission.strip().lower()
    perms = permissions_for_roles(roles)
    if permission in perms:
        return True
    domain = permission.split(":", 1)[0]
    return f"{domain}:*" in perms or "*:*" in perms
