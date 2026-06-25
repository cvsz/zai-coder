"""Release Automation and Update Center models.

All release/update operations are dry-run-first. This package does not publish
GitHub releases, push branches, mutate production systems, or apply updates.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class ReleaseVersion:
    version: str
    channel: str = "stable"
    previous_version: str = ""
    codename: str = "local-first"
    created_at: str = field(default_factory=now_iso)

    def validate(self) -> list[str]:
        issues: list[str] = []
        if not self.version.startswith("v"):
            issues.append("version must start with v")
        if self.channel not in {"dev", "alpha", "beta", "rc", "stable", "lts"}:
            issues.append("invalid release channel")
        if self.previous_version and not self.previous_version.startswith("v"):
            issues.append("previous_version must start with v")
        return issues

    def to_dict(self) -> dict:
        return self.__dict__.copy()


@dataclass(frozen=True)
class ReleasePlan:
    id: str
    version: ReleaseVersion
    package_name: str
    artifacts: tuple[str, ...]
    checks: tuple[str, ...]
    dry_run: bool = True
    created_at: str = field(default_factory=now_iso)

    def validate(self) -> list[str]:
        issues: list[str] = []
        issues.extend(self.version.validate())
        if not self.id or not self.package_name:
            issues.append("release plan id and package_name required")
        if not self.artifacts:
            issues.append("release plan requires at least one artifact")
        if not self.dry_run:
            issues.append("release plan must be dry-run by default")
        return issues

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "version": self.version.to_dict(),
            "package_name": self.package_name,
            "artifacts": list(self.artifacts),
            "checks": list(self.checks),
            "dry_run": self.dry_run,
            "created_at": self.created_at,
        }


@dataclass(frozen=True)
class UpdateManifest:
    id: str
    version: str
    channel: str
    package_name: str
    artifact_path: str
    sha256: str = ""
    size_bytes: int = 0
    min_current_version: str = "v1.0.0"
    rollback_supported: bool = True
    created_at: str = field(default_factory=now_iso)

    def validate(self) -> list[str]:
        issues: list[str] = []
        if not self.id or not self.version or not self.package_name:
            issues.append("manifest id, version, and package_name required")
        if self.channel not in {"dev", "alpha", "beta", "rc", "stable", "lts"}:
            issues.append("invalid channel")
        if not self.artifact_path:
            issues.append("artifact_path required")
        if not self.rollback_supported:
            issues.append("rollback must be supported by default")
        return issues

    def to_dict(self) -> dict:
        return self.__dict__.copy()


@dataclass(frozen=True)
class UpdateDecision:
    allowed: bool
    action: str
    reason: str
    required_backup: bool = True
    required_approval: bool = True
    dry_run: bool = True

    def to_dict(self) -> dict:
        return self.__dict__.copy()


@dataclass(frozen=True)
class ReleaseAuditEvent:
    id: str
    actor: str
    action: str
    target: str
    payload: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=now_iso)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "actor": self.actor,
            "action": self.action,
            "target": self.target,
            "payload": dict(self.payload),
            "created_at": self.created_at,
        }
