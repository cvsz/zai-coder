"""Role and permission matrix."""

from __future__ import annotations


ROLE_MATRIX = {
    "owner": ["*"],
    "admin": [
        "governance:view",
        "governance:approve",
        "execution:plan",
        "execution:apply",
        "providers:plan",
        "providers:apply",
        "observability:view",
    ],
    "operator": [
        "governance:view",
        "execution:plan",
        "execution:apply",
        "providers:plan",
        "observability:view",
    ],
    "auditor": [
        "governance:view",
        "audit:view",
        "observability:view",
        "evidence:view",
    ],
    "viewer": [
        "governance:view",
        "observability:view",
    ],
}


def permissions_for_role(role: str) -> list[str]:
    return ROLE_MATRIX.get(role, [])


def role_allows(role: str, permission: str) -> bool:
    perms = set(permissions_for_role(role))
    return "*" in perms or permission in perms


def role_matrix_manifest() -> dict:
    return {role: list(perms) for role, perms in ROLE_MATRIX.items()}
