"""Log retention policy."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class LogRetentionPolicy:
    hot_days: int = 7
    archive_days: int = 30
    max_log_mb: int = 256
    redact_secrets: bool = True
    include_paths: tuple[str, ...] = ("logs/", "data/")
    exclude_paths: tuple[str, ...] = (".git/", "node_modules/", "apps/zlms/", "backups/")

    def validate(self) -> list[str]:
        issues = []
        if self.hot_days < 1:
            issues.append("hot_days must be positive")
        if self.archive_days < self.hot_days:
            issues.append("archive_days must be >= hot_days")
        if self.max_log_mb < 1:
            issues.append("max_log_mb must be positive")
        return issues

    def to_dict(self) -> dict:
        return {
            "hot_days": self.hot_days,
            "archive_days": self.archive_days,
            "max_log_mb": self.max_log_mb,
            "redact_secrets": self.redact_secrets,
            "include_paths": list(self.include_paths),
            "exclude_paths": list(self.exclude_paths),
        }


def default_log_retention_policy() -> LogRetentionPolicy:
    return LogRetentionPolicy()
