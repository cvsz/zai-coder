"""Customer Portal and Onboarding models.

This package provides local-first customer portal and onboarding planning. It
does not send real emails, charge customers, provision cloud resources, or expose
customer data externally.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class CustomerAccount:
    id: str
    org_id: str
    name: str
    owner_email: str
    plan: str = "free"
    status: str = "trial"
    region: str = "global"
    created_at: str = field(default_factory=now_iso)

    def validate(self) -> list[str]:
        issues: list[str] = []
        if not self.id or not self.org_id or not self.name or not self.owner_email:
            issues.append("customer id, org_id, name, and owner_email required")
        if "@" not in self.owner_email:
            issues.append("invalid owner_email")
        if self.plan not in {"free", "pro", "enterprise", "internal"}:
            issues.append("invalid plan")
        if self.status not in {"trial", "active", "paused", "cancelled", "onboarding"}:
            issues.append("invalid customer status")
        return issues

    def to_dict(self) -> dict:
        return self.__dict__.copy()


@dataclass(frozen=True)
class PortalFeature:
    id: str
    name: str
    required_plan: str = "free"
    enabled: bool = True
    category: str = "portal"
    description: str = ""

    def validate(self) -> list[str]:
        issues: list[str] = []
        if not self.id or not self.name:
            issues.append("feature id and name required")
        if self.required_plan not in {"free", "pro", "enterprise", "internal"}:
            issues.append("invalid required_plan")
        if "/" in self.id or ".." in self.id:
            issues.append("unsafe feature id")
        return issues

    def to_dict(self) -> dict:
        return self.__dict__.copy()


@dataclass(frozen=True)
class OnboardingStep:
    id: str
    title: str
    description: str
    owner: str = "customer"
    required: bool = True
    status: str = "pending"
    order: int = 100

    def validate(self) -> list[str]:
        issues: list[str] = []
        if not self.id or not self.title:
            issues.append("step id and title required")
        if self.owner not in {"customer", "platform", "support", "billing"}:
            issues.append("invalid step owner")
        if self.status not in {"pending", "in_progress", "completed", "blocked", "skipped"}:
            issues.append("invalid step status")
        if self.order < 0:
            issues.append("order must be >= 0")
        return issues

    def to_dict(self) -> dict:
        return self.__dict__.copy()


@dataclass(frozen=True)
class OnboardingPlan:
    id: str
    customer_id: str
    org_id: str
    workspace_id: str
    steps: tuple[dict[str, Any], ...]
    dry_run: bool = True
    created_at: str = field(default_factory=now_iso)

    def validate(self) -> list[str]:
        issues: list[str] = []
        if not self.id or not self.customer_id or not self.org_id or not self.workspace_id:
            issues.append("plan id, customer_id, org_id, and workspace_id required")
        if not self.steps:
            issues.append("onboarding plan requires steps")
        if not self.dry_run:
            issues.append("onboarding plan must be dry-run by default")
        return issues

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "customer_id": self.customer_id,
            "org_id": self.org_id,
            "workspace_id": self.workspace_id,
            "steps": [dict(step) for step in self.steps],
            "dry_run": self.dry_run,
            "created_at": self.created_at,
        }


@dataclass(frozen=True)
class SupportTicket:
    id: str
    customer_id: str
    subject: str
    priority: str = "normal"
    status: str = "open"
    category: str = "general"
    created_by: str = "customer"
    created_at: str = field(default_factory=now_iso)

    def validate(self) -> list[str]:
        issues: list[str] = []
        if not self.id or not self.customer_id or not self.subject:
            issues.append("ticket id, customer_id, and subject required")
        if self.priority not in {"low", "normal", "high", "urgent"}:
            issues.append("invalid priority")
        if self.status not in {"open", "pending", "resolved", "closed"}:
            issues.append("invalid ticket status")
        if len(self.subject) > 300:
            issues.append("subject too large")
        return issues

    def to_dict(self) -> dict:
        return self.__dict__.copy()


@dataclass(frozen=True)
class CustomerAuditEvent:
    id: str
    actor: str
    action: str
    target: str
    customer_id: str = "cust_local"
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
            "customer_id": self.customer_id,
            "org_id": self.org_id,
            "workspace_id": self.workspace_id,
            "payload": dict(self.payload),
            "created_at": self.created_at,
        }
