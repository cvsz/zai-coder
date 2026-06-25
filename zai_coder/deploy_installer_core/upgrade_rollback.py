"""Upgrade and rollback plan helpers."""

from __future__ import annotations

from .config import DeployInstallConfig


def upgrade_plan(version: str = "v0.14.0", config: DeployInstallConfig | None = None) -> dict:
    config = config or DeployInstallConfig()
    return {
        "dry_run": True,
        "version": version,
        "commands": [
            "make verify-source-package",
            "make backup-plan",
            "make backup-create APPLY=1",
            f"git fetch --tags origin {version}",
            f"git checkout {version}",
            ".venv/bin/python -m pip install -r requirements-production.txt",
            "make production-migrate-plan",
            "make production-migrate-apply APPLY=1",
            f"sudo systemctl restart {config.app_name}.service",
            "make healthcheck",
        ],
    }


def rollback_plan(version: str = "previous", config: DeployInstallConfig | None = None) -> dict:
    config = config or DeployInstallConfig()
    return {
        "dry_run": True,
        "version": version,
        "commands": [
            "make backup-plan",
            f"git checkout {version}",
            ".venv/bin/python -m pip install -r requirements-production.txt",
            f"sudo systemctl restart {config.app_name}.service",
            "make healthcheck",
        ],
        "warnings": ["Rollback may require database restore if migrations are not backward-compatible."],
    }
