"""Usage Analytics and Insights models.

Analytics are local-first and privacy-safe. This package never phones home,
never exports raw PII by default, and keeps report generation reviewable.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class UsageEvent:
    id: str
    event_type: str
    customer_id: str
    org_id: str
    workspace_id: str
    actor_id: str = "anonymous"
    feature_id: str = "unknown"
    quantity: float = 1.0
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=now_iso)

    def validate(self) -> list[str]:
        issues: list[str] = []
        if not self.id or not self.event_type or not self.customer_id or not self.org_id or not self.workspace_id:
            issues.append("event id, event_type, customer_id, org_id, and workspace_id required")
        if self.quantity < 0:
            issues.append("quantity must be >= 0")
        forbidden_keys = {"email", "password", "token", "secret", "api_key", "credit_card"}
        if forbidden_keys & {str(key).lower() for key in self.metadata.keys()}:
            issues.append("metadata contains forbidden PII/secret key")
        return issues

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "event_type": self.event_type,
            "customer_id": self.customer_id,
            "org_id": self.org_id,
            "workspace_id": self.workspace_id,
            "actor_id": self.actor_id,
            "feature_id": self.feature_id,
            "quantity": self.quantity,
            "metadata": dict(self.metadata),
            "created_at": self.created_at,
        }


@dataclass(frozen=True)
class MetricSnapshot:
    id: str
    metric: str
    value: float
    period: str
    customer_id: str = "all"
    org_id: str = "all"
    workspace_id: str = "all"
    unit: str = "count"
    created_at: str = field(default_factory=now_iso)

    def validate(self) -> list[str]:
        issues: list[str] = []
        if not self.id or not self.metric or not self.period:
            issues.append("snapshot id, metric, and period required")
        if self.value < 0:
            issues.append("metric value must be >= 0")
        return issues

    def to_dict(self) -> dict:
        return self.__dict__.copy()


@dataclass(frozen=True)
class Insight:
    id: str
    title: str
    severity: str
    category: str
    summary: str
    recommendation: str = ""
    created_at: str = field(default_factory=now_iso)

    def validate(self) -> list[str]:
        issues: list[str] = []
        if not self.id or not self.title or not self.summary:
            issues.append("insight id, title, and summary required")
        if self.severity not in {"info", "low", "medium", "high"}:
            issues.append("invalid severity")
        if self.category not in {"adoption", "usage", "risk", "billing", "support", "growth", "quality"}:
            issues.append("invalid category")
        return issues

    def to_dict(self) -> dict:
        return self.__dict__.copy()


@dataclass(frozen=True)
class AnalyticsReport:
    id: str
    title: str
    period: str
    metrics: tuple[dict[str, Any], ...]
    insights: tuple[dict[str, Any], ...]
    dry_run: bool = True
    created_at: str = field(default_factory=now_iso)

    def validate(self) -> list[str]:
        issues: list[str] = []
        if not self.id or not self.title or not self.period:
            issues.append("report id, title, and period required")
        if not self.metrics:
            issues.append("report requires metrics")
        if not self.dry_run:
            issues.append("analytics report must be dry-run/export-only by default")
        return issues

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "period": self.period,
            "metrics": [dict(metric) for metric in self.metrics],
            "insights": [dict(insight) for insight in self.insights],
            "dry_run": self.dry_run,
            "created_at": self.created_at,
        }


@dataclass(frozen=True)
class AnalyticsAuditEvent:
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
