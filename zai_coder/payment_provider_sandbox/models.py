"""Payment Provider Sandbox models.

This package intentionally avoids real payment capture. It creates sandbox-only
plans, drafts, lifecycle events, and verifier scaffolds.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class PaymentProviderConfig:
    provider: str = "sandbox"
    mode: str = "sandbox"
    no_real_charge: bool = True
    webhook_tolerance_seconds: int = 300

    def validate(self) -> list[str]:
        issues: list[str] = []
        if self.provider not in {"sandbox", "stripe_sandbox", "mock"}:
            issues.append("provider must be sandbox, stripe_sandbox, or mock")
        if self.mode != "sandbox":
            issues.append("only sandbox mode is allowed")
        if not self.no_real_charge:
            issues.append("no_real_charge must remain true")
        if self.webhook_tolerance_seconds <= 0:
            issues.append("webhook tolerance must be positive")
        return issues

    def to_dict(self) -> dict:
        return self.__dict__.copy()


@dataclass(frozen=True)
class CheckoutSessionDraft:
    id: str
    org_id: str
    plan_id: str
    amount_cents: int
    currency: str = "USD"
    status: str = "draft"
    success_url: str = "http://127.0.0.1:8765/billing/success"
    cancel_url: str = "http://127.0.0.1:8765/billing/cancel"
    provider: str = "sandbox"
    created_at: str = field(default_factory=now_iso)

    def validate(self) -> list[str]:
        issues = []
        if not self.id or not self.org_id or not self.plan_id:
            issues.append("checkout id, org_id, and plan_id required")
        if self.amount_cents < 0:
            issues.append("amount must be >= 0")
        if self.currency not in {"USD", "THB"}:
            issues.append("unsupported currency")
        if self.status not in {"draft", "created", "expired", "completed", "cancelled"}:
            issues.append("invalid status")
        if not self.success_url.startswith("http://127.0.0.1") and not self.success_url.startswith("http://localhost"):
            issues.append("success_url must be localhost-first in sandbox")
        return issues

    def to_dict(self) -> dict:
        return self.__dict__.copy()


@dataclass(frozen=True)
class SubscriptionRecord:
    id: str
    org_id: str
    plan_id: str
    status: str = "trialing"
    provider_subscription_id: str = "sandbox_sub"
    current_period_start: str = field(default_factory=now_iso)
    current_period_end: str = ""
    created_at: str = field(default_factory=now_iso)

    def validate(self) -> list[str]:
        issues = []
        if self.status not in {"trialing", "active", "past_due", "cancelled", "incomplete", "paused"}:
            issues.append("invalid subscription status")
        if not self.id or not self.org_id or not self.plan_id:
            issues.append("subscription id, org_id, and plan_id required")
        return issues

    def to_dict(self) -> dict:
        return self.__dict__.copy()


@dataclass(frozen=True)
class PaymentAuditEvent:
    id: str
    org_id: str
    actor: str
    action: str
    target: str
    provider: str = "sandbox"
    payload: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=now_iso)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "org_id": self.org_id,
            "actor": self.actor,
            "action": self.action,
            "target": self.target,
            "provider": self.provider,
            "payload": dict(self.payload),
            "created_at": self.created_at,
        }


@dataclass(frozen=True)
class WebhookEventDraft:
    id: str
    provider: str
    event_type: str
    org_id: str
    payload: dict[str, Any]
    signature: str = ""
    created_at: str = field(default_factory=now_iso)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "provider": self.provider,
            "event_type": self.event_type,
            "org_id": self.org_id,
            "payload": dict(self.payload),
            "signature": self.signature,
            "created_at": self.created_at,
        }
