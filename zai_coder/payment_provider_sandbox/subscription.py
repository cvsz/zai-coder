"""Subscription lifecycle model."""

from __future__ import annotations

import uuid

from .models import SubscriptionRecord


ALLOWED_TRANSITIONS = {
    "trialing": {"active", "cancelled", "past_due"},
    "active": {"past_due", "cancelled", "paused"},
    "past_due": {"active", "cancelled"},
    "paused": {"active", "cancelled"},
    "incomplete": {"active", "cancelled"},
    "cancelled": set(),
}


def create_subscription(org_id: str, plan_id: str, status: str = "trialing") -> SubscriptionRecord:
    record = SubscriptionRecord(id=f"sub_sandbox_{uuid.uuid4().hex[:12]}", org_id=org_id, plan_id=plan_id, status=status)
    issues = record.validate()
    if issues:
        raise ValueError("; ".join(issues))
    return record


def transition_subscription(subscription: SubscriptionRecord, new_status: str) -> SubscriptionRecord:
    allowed = ALLOWED_TRANSITIONS.get(subscription.status, set())
    if new_status not in allowed:
        raise ValueError(f"invalid subscription transition: {subscription.status} -> {new_status}")
    return SubscriptionRecord(
        id=subscription.id,
        org_id=subscription.org_id,
        plan_id=subscription.plan_id,
        status=new_status,
        provider_subscription_id=subscription.provider_subscription_id,
        current_period_start=subscription.current_period_start,
        current_period_end=subscription.current_period_end,
        created_at=subscription.created_at,
    )


def subscription_lifecycle_manifest() -> dict:
    return {key: sorted(value) for key, value in ALLOWED_TRANSITIONS.items()}
