"""Plan upgrade/downgrade workflow."""

from __future__ import annotations

from zai_coder.billing_usage_enforcement.plans import get_plan


def plan_change_workflow(org_id: str, current_plan_id: str, target_plan_id: str) -> dict:
    current = get_plan(current_plan_id)
    target = get_plan(target_plan_id)
    direction = "upgrade" if target.monthly_price_cents >= current.monthly_price_cents else "downgrade"
    return {
        "dry_run": True,
        "org_id": org_id,
        "current_plan": current.to_dict(),
        "target_plan": target.to_dict(),
        "direction": direction,
        "steps": [
            "validate tenant billing account",
            "check current usage against target plan",
            "create checkout session draft if price increases",
            "record payment audit event",
            "apply plan change only after sandbox confirmation",
            "notify billing contact",
        ],
    }


def failed_payment_policy(plan_id: str = "pro") -> dict:
    return {
        "plan_id": plan_id,
        "grace_period_days": 7,
        "actions": [
            "send payment failed email",
            "mark billing account past_due",
            "limit provider apply operations after grace period",
            "keep data available for export",
            "never delete tenant data automatically",
        ],
        "safe_mode": True,
    }
