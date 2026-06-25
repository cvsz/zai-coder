"""Billing handoff draft.

No payment provider calls are made and no real charges are created.
"""

from __future__ import annotations


def billing_handoff_draft(customer: dict) -> dict:
    return {
        "dry_run": True,
        "customer_id": customer["id"],
        "org_id": customer["org_id"],
        "plan": customer["plan"],
        "billing_mode": "draft-only",
        "no_real_charge": True,
        "steps": [
            "show plan summary",
            "show quota summary",
            "show draft billing terms",
            "route upgrades to payment sandbox",
            "require explicit payment-provider approval for real billing integration",
        ],
    }


def upgrade_request_plan(customer: dict, target_plan: str = "pro") -> dict:
    blocked = []
    if target_plan not in {"free", "pro", "enterprise"}:
        blocked.append("invalid target plan")
    if customer["plan"] == target_plan:
        blocked.append("already on target plan")
    return {
        "dry_run": True,
        "allowed": not blocked,
        "blocked": blocked,
        "customer_id": customer["id"],
        "current_plan": customer["plan"],
        "target_plan": target_plan,
        "payment_capture": False,
    }
