"""Multi-tenant control models."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class TenantOrg:
    id: str
    name: str
    slug: str
    status: str = "active"
    created_at: str = field(default_factory=now_iso)

    def validate(self) -> list[str]:
        issues: list[str] = []
        if not self.id or not self.name or not self.slug:
            issues.append("tenant id, name, and slug required")
        if self.status not in {"active", "suspended", "archived"}:
            issues.append("invalid tenant status")
        if "/" in self.slug or ".." in self.slug:
            issues.append("unsafe tenant slug")
        return issues

    def to_dict(self) -> dict:
        return self.__dict__.copy()


@dataclass(frozen=True)
class Workspace:
    id: str
    org_id: str
    name: str
    slug: str
    status: str = "active"
    created_at: str = field(default_factory=now_iso)

    def validate(self) -> list[str]:
        issues: list[str] = []
        if not self.id or not self.org_id or not self.name or not self.slug:
            issues.append("workspace id, org_id, name, and slug required")
        if self.status not in {"active", "suspended", "archived"}:
            issues.append("invalid workspace status")
        if "/" in self.slug or ".." in self.slug:
            issues.append("unsafe workspace slug")
        return issues

    def to_dict(self) -> dict:
        return self.__dict__.copy()


@dataclass(frozen=True)
class TenantPrincipal:
    actor: str
    org_id: str
    workspace_id: str
    roles: tuple[str, ...] = ("viewer",)
    created_at: str = field(default_factory=now_iso)

    def to_dict(self) -> dict:
        return {
            "actor": self.actor,
            "org_id": self.org_id,
            "workspace_id": self.workspace_id,
            "roles": list(self.roles),
            "created_at": self.created_at,
        }


@dataclass(frozen=True)
class TenantScopedApiKey:
    id: str
    org_id: str
    workspace_id: str
    name: str
    token_prefix: str
    scopes: tuple[str, ...]
    status: str = "active"
    created_at: str = field(default_factory=now_iso)

    def to_public_dict(self) -> dict:
        return {
            "id": self.id,
            "org_id": self.org_id,
            "workspace_id": self.workspace_id,
            "name": self.name,
            "token_prefix": self.token_prefix,
            "scopes": list(self.scopes),
            "status": self.status,
            "created_at": self.created_at,
        }


@dataclass(frozen=True)
class TenantAuditEvent:
    id: str
    org_id: str
    workspace_id: str
    actor: str
    action: str
    target: str
    payload: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=now_iso)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "org_id": self.org_id,
            "workspace_id": self.workspace_id,
            "actor": self.actor,
            "action": self.action,
            "target": self.target,
            "payload": dict(self.payload),
            "created_at": self.created_at,
        }


@dataclass(frozen=True)
class WorkspaceQuota:
    org_id: str
    workspace_id: str
    monthly_runs_limit: int = 1000
    storage_mb_limit: int = 1024
    provider_apply_limit: int = 100

    def validate(self) -> list[str]:
        issues = []
        if self.monthly_runs_limit < 0:
            issues.append("monthly_runs_limit must be >= 0")
        if self.storage_mb_limit < 0:
            issues.append("storage_mb_limit must be >= 0")
        if self.provider_apply_limit < 0:
            issues.append("provider_apply_limit must be >= 0")
        return issues

    def to_dict(self) -> dict:
        return self.__dict__.copy()
