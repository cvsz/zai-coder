"""Operations Control Center models."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class ServiceStatus:
    name: str
    target: str
    status: str
    detail: str = ""
    checked_at: str = field(default_factory=now_iso)

    def validate(self) -> list[str]:
        issues: list[str] = []
        if not self.name:
            issues.append("service name required")
        if self.target not in {"systemd", "docker", "local", "cloudflare", "database", "unknown"}:
            issues.append(f"invalid target: {self.target}")
        if self.status not in {"unknown", "planned", "running", "stopped", "degraded", "failed", "blocked"}:
            issues.append(f"invalid status: {self.status}")
        return issues

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "target": self.target,
            "status": self.status,
            "detail": self.detail,
            "checked_at": self.checked_at,
        }


@dataclass(frozen=True)
class OperationPlan:
    name: str
    action: str
    commands: tuple[str, ...] = ()
    dry_run: bool = True
    requires_backup: bool = False
    requires_approval: bool = True
    warnings: tuple[str, ...] = ()

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "action": self.action,
            "commands": list(self.commands),
            "dry_run": self.dry_run,
            "requires_backup": self.requires_backup,
            "requires_approval": self.requires_approval,
            "warnings": list(self.warnings),
        }


@dataclass(frozen=True)
class HealthSignal:
    name: str
    ok: bool
    value: str = ""
    severity: str = "info"

    def to_dict(self) -> dict:
        return {"name": self.name, "ok": self.ok, "value": self.value, "severity": self.severity}
