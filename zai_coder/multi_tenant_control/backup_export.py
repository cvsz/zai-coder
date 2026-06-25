"""Tenant backup/export policy."""

from __future__ import annotations

from pathlib import Path


def tenant_export_path(org_slug: str, workspace_slug: str) -> str:
    for part in (org_slug, workspace_slug):
        if not part or "/" in part or ".." in part:
            raise ValueError("unsafe tenant/workspace slug")
    return f"exports/tenants/{org_slug}/{workspace_slug}/export.json"


def tenant_backup_policy(org_slug: str = "local-org", workspace_slug: str = "default") -> dict:
    return {
        "dry_run": True,
        "org_slug": org_slug,
        "workspace_slug": workspace_slug,
        "export_path": tenant_export_path(org_slug, workspace_slug),
        "include": ["workspace metadata", "tenant audit events", "quota settings", "non-secret config"],
        "exclude": [".env", "credentials.json", "tokens", "node_modules", ".git", "apps/zlms"],
        "retention_days": 14,
    }


def write_tenant_export(payload: dict, org_slug: str = "local-org", workspace_slug: str = "default", root: str | Path = ".") -> str:
    root = Path(root)
    path = root / tenant_export_path(org_slug, workspace_slug)
    path.parent.mkdir(parents=True, exist_ok=True)
    import json
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    return str(path)
