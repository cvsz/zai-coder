"""Plugin Connector Hub models.

Connector operations are local-first, dry-run-first, tenant-scoped, and audited.
No external connector call is made by this package.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class ConnectorManifest:
    id: str
    name: str
    provider: str
    version: str
    description: str
    category: str = "general"
    required_env: tuple[str, ...] = ()
    required_permissions: tuple[str, ...] = ("connector:view",)
    supported_actions: tuple[str, ...] = ("status",)
    webhook_supported: bool = False
    sync_supported: bool = True
    created_at: str = field(default_factory=now_iso)

    def validate(self) -> list[str]:
        issues: list[str] = []
        if not self.id or not self.name or not self.provider or not self.version:
            issues.append("connector id, name, provider, and version required")
        if "/" in self.id or ".." in self.id:
            issues.append("unsafe connector id")
        if any(key.startswith("LIVE_") or key.endswith("_LIVE_SECRET") for key in self.required_env):
            issues.append("live secret env keys are not allowed by default")
        if any("/" in perm or ".." in perm for perm in self.required_permissions):
            issues.append("unsafe permission value")
        return issues

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "provider": self.provider,
            "version": self.version,
            "description": self.description,
            "category": self.category,
            "required_env": list(self.required_env),
            "required_permissions": list(self.required_permissions),
            "supported_actions": list(self.supported_actions),
            "webhook_supported": self.webhook_supported,
            "sync_supported": self.sync_supported,
            "created_at": self.created_at,
        }


@dataclass(frozen=True)
class ConnectorInstallation:
    id: str
    connector_id: str
    org_id: str
    workspace_id: str
    enabled: bool = False
    installed_by: str = "system"
    installed_at: str = field(default_factory=now_iso)

    def validate(self) -> list[str]:
        issues: list[str] = []
        if not self.id or not self.connector_id:
            issues.append("installation id and connector_id required")
        if not self.org_id or not self.workspace_id:
            issues.append("tenant context required")
        return issues

    def to_dict(self) -> dict:
        return self.__dict__.copy()


@dataclass(frozen=True)
class ConnectorSyncPlan:
    id: str
    connector_id: str
    org_id: str
    workspace_id: str
    action: str
    dry_run: bool = True
    steps: tuple[str, ...] = ()
    created_at: str = field(default_factory=now_iso)

    def validate(self) -> list[str]:
        issues: list[str] = []
        if not self.id or not self.connector_id or not self.action:
            issues.append("sync plan id, connector_id, and action required")
        if not self.dry_run:
            issues.append("connector sync plans must be dry-run by default")
        return issues

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "connector_id": self.connector_id,
            "org_id": self.org_id,
            "workspace_id": self.workspace_id,
            "action": self.action,
            "dry_run": self.dry_run,
            "steps": list(self.steps),
            "created_at": self.created_at,
        }


@dataclass(frozen=True)
class ConnectorAuditEvent:
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
class WebhookIngressDraft:
    id: str
    connector_id: str
    event_type: str
    org_id: str
    workspace_id: str
    payload_schema: dict[str, Any] = field(default_factory=dict)
    secret_env: str = ""
    created_at: str = field(default_factory=now_iso)

    def validate(self) -> list[str]:
        issues: list[str] = []
        if not self.id or not self.connector_id or not self.event_type:
            issues.append("webhook id, connector_id, and event_type required")
        if self.secret_env and not self.secret_env.endswith("_WEBHOOK_SECRET"):
            issues.append("webhook secret env should end with _WEBHOOK_SECRET")
        return issues

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "connector_id": self.connector_id,
            "event_type": self.event_type,
            "org_id": self.org_id,
            "workspace_id": self.workspace_id,
            "payload_schema": dict(self.payload_schema),
            "secret_env": self.secret_env,
            "created_at": self.created_at,
        }
