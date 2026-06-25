"""Tenant isolation policy."""

from __future__ import annotations


TENANT_ISOLATION_RULES = [
    "Every organization has isolated workspace identifiers.",
    "Every API key is scoped to an organization/workspace.",
    "Audit events include actor and target.",
    "Provider operations must include actor and approval context.",
    "Backups must not mix unrelated tenant exports.",
    "Admin actions require elevated role.",
]


def tenant_isolation_policy() -> dict:
    return {"rules": TENANT_ISOLATION_RULES, "required": True}


def tenant_isolation_check(payload: dict) -> dict:
    missing = []
    for field in ("organization_id", "workspace_id", "actor"):
        if not payload.get(field):
            missing.append(field)
    return {"ok": not missing, "missing": missing, "rules": TENANT_ISOLATION_RULES}
