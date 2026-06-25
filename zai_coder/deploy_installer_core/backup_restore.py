"""Deploy installer backup/restore policy and plans."""

from __future__ import annotations

from pathlib import Path

from .config import DeployInstallConfig


def backup_plan(config: DeployInstallConfig | None = None) -> dict:
    config = config or DeployInstallConfig()
    return {
        "dry_run": True,
        "archive": f"{config.backup_dir}/{config.app_name}-backup.tar.gz",
        "include": [config.data_dir, config.logs_dir, config.storage_dir],
        "exclude": ["release", "node_modules", ".git", "apps/zlms"],
        "commands": [
            f"mkdir -p {config.backup_dir}",
            f"tar --exclude=release --exclude=node_modules --exclude=.git --exclude=apps/zlms -czf {config.backup_dir}/{config.app_name}-backup.tar.gz {config.data_dir} {config.logs_dir} {config.storage_dir}",
        ],
    }


def restore_plan(archive: str, config: DeployInstallConfig | None = None) -> dict:
    config = config or DeployInstallConfig()
    if not archive or Path(archive).is_absolute() or ".." in Path(archive).parts:
        raise ValueError("archive must be a safe relative path")
    return {
        "dry_run": True,
        "archive": archive,
        "commands": [
            "make backup-plan",
            f"tar -tzf {archive}",
            f"tar -xzf {archive} -C .",
            "make healthcheck",
        ],
        "warnings": ["Create a fresh backup before restore.", "Inspect archive listing before extraction."],
    }
