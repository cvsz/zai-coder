"""Admin export helpers."""

from __future__ import annotations

import json
from pathlib import Path

from .directory import tenant_directory, workspace_directory, user_directory
from .feature_flags import feature_flag_catalog
from .config_registry import config_registry
from .service_control import service_catalog
from .rbac import role_matrix


def admin_export_bundle() -> dict:
    return {
        "kind": "zai-admin-console-export",
        "version": "1.0",
        "tenants": tenant_directory(),
        "workspaces": workspace_directory(),
        "users": user_directory(),
        "feature_flags": feature_flag_catalog(),
        "config": config_registry(),
        "services": service_catalog(),
        "roles": role_matrix(),
        "safe_export": True,
        "secrets_redacted": True,
    }


def write_admin_export(root: str | Path = ".", out: str = "admin/exports/admin-console-export.json") -> str:
    root = Path(root)
    path = root / out
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(admin_export_bundle(), indent=2, sort_keys=True), encoding="utf-8")
    return str(path)
