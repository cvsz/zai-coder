"""Self-Healing Operations models.

Self-healing is policy-first and dry-run-first. No destructive remediation is
executed automatically; plans must pass guardrails and approval gates.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class HealthSignal:
    id: str
    source: str
    metric: str
    value: float
    status: str = "ok"
    service: str = "core"
    org_id: str = "org_local"
    workspace_id: str = "ws_default"
    observed_at: str = field(default_factory=now_iso)

    def validate(self) -> list[str]:
        issues: list[str] = []
        if not self.id or not self.source or not self.metric:
            issues.append("signal id, source, and metric required")
        if self.status not in {"ok", "warning", "critical", "unknown"}:
            issues.append("invalid signal status")
        if self.value < 0:
            issues.append("signal value must be >= 0")
        return issues

    def to_dict(self) -> dict:
        return self.__dict__.copy()


@dataclass(frozen=True)
class Incident:
    id: str
    title: str
    severity: str
    service: str
    status: str = "open"
    signals: tuple[dict[str, Any], ...] = ()
    org_id: str = "org_local"
    workspace_id: str = "ws_default"
    created_at: str = field(default_factory=now_iso)

    def validate(self) -> list[str]:
        issues: list[str] = []
        if not self.id or not self.title or not self.service:
            issues.append("incident id, title, and service required")
        if self.severity not in {"low", "medium", "high", "critical"}:
            issues.append("invalid severity")
        if self.status not in {"open", "investigating", "mitigating", "resolved", "closed"}:
            issues.append("invalid incident status")
        return issues

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "severity": self.severity,
            "service": self.service,
            "status": self.status,
            "signals": [dict(signal) for signal in self.signals],
            "org_id": self.org_id,
            "workspace_id": self.workspace_id,
            "created_at": self.created_at,
        }


@dataclass(frozen=True)
class RemediationPlaybook:
    id: str
    name: str
    service: str
    trigger: str
    actions: tuple[str, ...]
    risk_level: str = "low"
    rollback_required: bool = True
    approval_required: bool = True

    def validate(self) -> list[str]:
        issues: list[str] = []
        if not self.id or not self.name or not self.service or not self.trigger:
            issues.append("playbook id, name, service, and trigger required")
        if self.risk_level not in {"low", "medium", "high"}:
            issues.append("invalid risk level")
        if not self.actions:
            issues.append("playbook actions required")
        forbidden = {"rm -rf", "drop database", "force push", "--no-verify"}
        if any(any(pattern in action.lower() for pattern in forbidden) for action in self.actions):
            issues.append("playbook contains forbidden action")
        return issues

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "service": self.service,
            "trigger": self.trigger,
            "actions": list(self.actions),
            "risk_level": self.risk_level,
            "rollback_required": self.rollback_required,
            "approval_required": self.approval_required,
        }


@dataclass(frozen=True)
class HealingPlan:
    id: str
    incident_id: str
    playbook_id: str
    actions: tuple[str, ...]
    dry_run: bool = True
    approval_id: str = ""
    rollback_plan: tuple[str, ...] = ()
    created_at: str = field(default_factory=now_iso)

    def validate(self) -> list[str]:
        issues: list[str] = []
        if not self.id or not self.incident_id or not self.playbook_id:
            issues.append("healing plan id, incident_id, and playbook_id required")
        if not self.dry_run:
            issues.append("healing plan must be dry-run by default")
        if not self.rollback_plan:
            issues.append("rollback plan required")
        return issues

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "incident_id": self.incident_id,
            "playbook_id": self.playbook_id,
            "actions": list(self.actions),
            "dry_run": self.dry_run,
            "approval_id": self.approval_id,
            "rollback_plan": list(self.rollback_plan),
            "created_at": self.created_at,
        }


@dataclass(frozen=True)
class HealingAuditEvent:
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
