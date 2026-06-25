"""Enterprise Admin Console models.

The admin console is safe-by-default: read-only previews, redacted secrets,
tenant-scoped access, and APPLY/approval gates for demo mutations.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class AdminUser:
    id: str
    email: str
    display_name: str
    roles: tuple[str, ...] = ("viewer",)
    status: str = "active"
    org_id: str = "org_local"
    workspace_id: str = "ws_default"
    created_at: str = field(default_factory=now_iso)

    def validate(self) -> list[str]:
        issues: list[str] = []
        if not self.id or not self.email or not self.display_name:
            issues.append("user id, email, and display_name required")
        if "@" not in self.email:
            issues.append("invalid email")
        if self.status not in {"active", "suspended", "invited", "disabled"}:
            issues.append("invalid user status")
        if not self.org_id or not self.workspace_id:
            issues.append("tenant context required")
        return issues

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "email": self.email,
            "display_name": self.display_name,
            "roles": list(self.roles),
            "status": self.status,
            "org_id": self.org_id,
            "workspace_id": self.workspace_id,
            "created_at": self.created_at,
        }


@dataclass(frozen=True)
class AdminTenant:
    id: str
    name: str
    plan: str = "free"
    status: str = "active"
    region: str = "global"
    created_at: str = field(default_factory=now_iso)

    def validate(self) -> list[str]:
        issues: list[str] = []
        if not self.id or not self.name:
            issues.append("tenant id and name required")
        if self.plan not in {"free", "pro", "enterprise", "internal"}:
            issues.append("invalid plan")
        if self.status not in {"active", "suspended", "trial", "disabled"}:
            issues.append("invalid tenant status")
        return issues

    def to_dict(self) -> dict:
        return self.__dict__.copy()


@dataclass(frozen=True)
class AdminWorkspace:
    id: str
    org_id: str
    name: str
    status: str = "active"
    quota_profile: str = "default"
    created_at: str = field(default_factory=now_iso)

    def validate(self) -> list[str]:
        issues: list[str] = []
        if not self.id or not self.org_id or not self.name:
            issues.append("workspace id, org_id, and name required")
        if self.status not in {"active", "archived", "suspended"}:
            issues.append("invalid workspace status")
        return issues

    def to_dict(self) -> dict:
        return self.__dict__.copy()


@dataclass(frozen=True)
class FeatureFlag:
    id: str
    name: str
    enabled: bool = False
    scope: str = "global"
    owner: str = "platform"
    description: str = ""

    def validate(self) -> list[str]:
        issues: list[str] = []
        if not self.id or not self.name:
            issues.append("feature flag id and name required")
        if self.scope not in {"global", "org", "workspace", "user"}:
            issues.append("invalid flag scope")
        if "/" in self.id or ".." in self.id:
            issues.append("unsafe flag id")
        return issues

    def to_dict(self) -> dict:
        return self.__dict__.copy()


@dataclass(frozen=True)
class ConfigEntry:
    key: str
    value: str
    category: str = "general"
    secret: bool = False
    mutable: bool = False

    def validate(self) -> list[str]:
        issues: list[str] = []
        if not self.key:
            issues.append("config key required")
        if "/" in self.key or ".." in self.key:
            issues.append("unsafe config key")
        if self.secret and self.value and self.value != "<redacted>":
            issues.append("secret values must be redacted")
        return issues

    def to_dict(self) -> dict:
        return {
            "key": self.key,
            "value": "<redacted>" if self.secret else self.value,
            "category": self.category,
            "secret": self.secret,
            "mutable": self.mutable,
        }


@dataclass(frozen=True)
class ServiceActionPlan:
    id: str
    service: str
    action: str
    steps: tuple[str, ...]
    dry_run: bool = True
    approval_required: bool = True

    def validate(self) -> list[str]:
        issues: list[str] = []
        if not self.id or not self.service or not self.action:
            issues.append("service action plan id, service, and action required")
        if self.action not in {"status", "restart-plan", "drain-plan", "backup-plan", "rollback-plan", "healthcheck"}:
            issues.append("unsupported service action")
        if not self.dry_run:
            issues.append("service action plans must be dry-run by default")
        forbidden = ("rm -rf", "drop database", "force push", "--no-verify")
        if any(any(pattern in step.lower() for pattern in forbidden) for step in self.steps):
            issues.append("service action contains forbidden step")
        return issues

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "service": self.service,
            "action": self.action,
            "steps": list(self.steps),
            "dry_run": self.dry_run,
            "approval_required": self.approval_required,
        }


@dataclass(frozen=True)
class AdminAuditEvent:
    id: str
    actor: str
    action: str
    target: str
    org_id: str = "org_local"
    workspace_id: str = "ws_default"
    payload: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=now_iso)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "actor": self.actor,
            "action": self.action,
            "target": self.target,
            "org_id": self.org_id,
            "workspace_id": self.workspace_id,
            "payload": dict(self.payload),
            "created_at": self.created_at,
        }
