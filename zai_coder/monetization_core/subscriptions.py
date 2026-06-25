"""Subscription state model.

This module is provider-neutral and local-first.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


VALID_SUBSCRIPTION_STATUSES = {
    "trialing",
    "active",
    "past_due",
    "paused",
    "cancelled",
    "expired",
}


@dataclass
class Subscription:
    id: str
    account_id: str
    plan_slug: str
    status: str = "active"
    provider: str = "local"
    provider_subscription_id: str = ""
    started_at: str = field(default_factory=now_iso)
    current_period_start: str = field(default_factory=now_iso)
    current_period_end: str = ""
    cancel_at_period_end: bool = False

    def validate(self) -> list[str]:
        issues: list[str] = []
        if not self.id:
            issues.append("missing id")
        if not self.account_id:
            issues.append("missing account_id")
        if not self.plan_slug:
            issues.append("missing plan_slug")
        if self.status not in VALID_SUBSCRIPTION_STATUSES:
            issues.append(f"invalid status: {self.status}")
        return issues

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "account_id": self.account_id,
            "plan_slug": self.plan_slug,
            "status": self.status,
            "provider": self.provider,
            "provider_subscription_id": self.provider_subscription_id,
            "started_at": self.started_at,
            "current_period_start": self.current_period_start,
            "current_period_end": self.current_period_end,
            "cancel_at_period_end": self.cancel_at_period_end,
        }
