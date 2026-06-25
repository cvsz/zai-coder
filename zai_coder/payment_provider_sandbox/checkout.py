"""Sandbox checkout session drafts."""

from __future__ import annotations

import uuid

from zai_coder.billing_usage_enforcement.plans import get_plan
from .models import CheckoutSessionDraft, PaymentProviderConfig


def create_checkout_session_draft(org_id: str, plan_id: str, provider: str = "sandbox") -> CheckoutSessionDraft:
    config = PaymentProviderConfig(provider=provider)
    issues = config.validate()
    if issues:
        raise ValueError("; ".join(issues))
    plan = get_plan(plan_id)
    draft = CheckoutSessionDraft(
        id=f"cs_sandbox_{uuid.uuid4().hex[:12]}",
        org_id=org_id,
        plan_id=plan_id,
        amount_cents=plan.monthly_price_cents,
        provider=provider,
    )
    draft_issues = draft.validate()
    if draft_issues:
        raise ValueError("; ".join(draft_issues))
    return draft


def checkout_session_payload(draft: CheckoutSessionDraft) -> dict:
    return {
        "provider": draft.provider,
        "mode": "sandbox",
        "no_real_charge": True,
        "checkout": draft.to_dict(),
        "instructions": [
            "Review checkout draft.",
            "No payment provider is called.",
            "Use sandbox webhook draft to simulate completion.",
        ],
    }
