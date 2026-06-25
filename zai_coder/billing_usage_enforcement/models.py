"""Billing and usage enforcement models."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class BillingAccount:
    id: str
    org_id: str
    plan_id: str
    status: str = "active"
    billing_email: str = "billing@example.com"
    currency: str = "USD"
    created_at: str = field(default_factory=now_iso)

    def validate(self) -> list[str]:
        issues: list[str] = []
        if not self.id or not self.org_id or not self.plan_id:
            issues.append("billing account id, org_id, and plan_id required")
        if self.status not in {"trial", "active", "past_due", "suspended", "cancelled"}:
            issues.append("invalid billing status")
        if "@" not in self.billing_email:
            issues.append("billing_email must be valid")
        if self.currency not in {"USD", "THB"}:
            issues.append("unsupported currency")
        return issues

    def to_dict(self) -> dict:
        return self.__dict__.copy()


@dataclass(frozen=True)
class BillingPlan:
    id: str
    name: str
    monthly_price_cents: int
    monthly_runs_limit: int
    storage_mb_limit: int
    provider_apply_limit: int
    seats_limit: int
    support_level: str = "community"

    def validate(self) -> list[str]:
        issues: list[str] = []
        if not self.id or not self.name:
            issues.append("plan id and name required")
        for key, value in {
            "monthly_price_cents": self.monthly_price_cents,
            "monthly_runs_limit": self.monthly_runs_limit,
            "storage_mb_limit": self.storage_mb_limit,
            "provider_apply_limit": self.provider_apply_limit,
            "seats_limit": self.seats_limit,
        }.items():
            if value < 0:
                issues.append(f"{key} must be >= 0")
        return issues

    def to_dict(self) -> dict:
        return self.__dict__.copy()


@dataclass(frozen=True)
class UsageEvent:
    id: str
    org_id: str
    workspace_id: str
    event_type: str
    quantity: int = 1
    unit: str = "count"
    actor: str = "system"
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=now_iso)

    def validate(self) -> list[str]:
        issues = []
        if not self.id or not self.org_id or not self.workspace_id:
            issues.append("usage event id, org_id, and workspace_id required")
        if self.quantity < 0:
            issues.append("quantity must be >= 0")
        if self.event_type not in {"run", "provider_apply", "storage_mb", "seat", "api_call"}:
            issues.append("invalid event_type")
        return issues

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "org_id": self.org_id,
            "workspace_id": self.workspace_id,
            "event_type": self.event_type,
            "quantity": self.quantity,
            "unit": self.unit,
            "actor": self.actor,
            "metadata": dict(self.metadata),
            "created_at": self.created_at,
        }


@dataclass(frozen=True)
class WorkspaceUsageSummary:
    org_id: str
    workspace_id: str
    monthly_runs: int = 0
    storage_mb: int = 0
    provider_apply: int = 0
    seats: int = 0
    api_calls: int = 0

    def to_dict(self) -> dict:
        return self.__dict__.copy()


@dataclass(frozen=True)
class InvoiceDraft:
    id: str
    org_id: str
    plan_id: str
    currency: str
    subtotal_cents: int
    overage_cents: int
    total_cents: int
    line_items: tuple[dict[str, Any], ...]
    created_at: str = field(default_factory=now_iso)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "org_id": self.org_id,
            "plan_id": self.plan_id,
            "currency": self.currency,
            "subtotal_cents": self.subtotal_cents,
            "overage_cents": self.overage_cents,
            "total_cents": self.total_cents,
            "line_items": [dict(item) for item in self.line_items],
            "created_at": self.created_at,
        }


@dataclass(frozen=True)
class BillingAuditEvent:
    id: str
    org_id: str
    actor: str
    action: str
    target: str
    payload: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=now_iso)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "org_id": self.org_id,
            "actor": self.actor,
            "action": self.action,
            "target": self.target,
            "payload": dict(self.payload),
            "created_at": self.created_at,
        }
