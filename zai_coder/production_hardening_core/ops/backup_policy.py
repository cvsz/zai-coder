"""Production backup policy."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BackupPolicy:
    schedule: str = "daily"
    retention_days: int = 14
    include_paths: tuple[str, ...] = ("data/", "logs/", "storage/")
    exclude_paths: tuple[str, ...] = ("release/", "node_modules/", ".git/", "apps/zlms/")
    encryption_required: bool = True
    restore_test_required: bool = True

    def validate(self) -> list[str]:
        issues = []
        if self.schedule not in {"hourly", "daily", "weekly"}:
            issues.append("unsupported schedule")
        if self.retention_days < 1:
            issues.append("retention_days must be positive")
        if not self.include_paths:
            issues.append("include_paths required")
        return issues

    def to_dict(self) -> dict:
        return {
            "schedule": self.schedule,
            "retention_days": self.retention_days,
            "include_paths": list(self.include_paths),
            "exclude_paths": list(self.exclude_paths),
            "encryption_required": self.encryption_required,
            "restore_test_required": self.restore_test_required,
        }


def default_backup_policy() -> BackupPolicy:
    return BackupPolicy()
