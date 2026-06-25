"""Billing plans and plan policy."""

from __future__ import annotations

from .models import BillingPlan


DEFAULT_PLANS = {
    "trial": BillingPlan("trial", "Trial", 0, 100, 256, 5, 1, "community"),
    "free": BillingPlan("free", "Free", 0, 250, 512, 10, 1, "community"),
    "pro": BillingPlan("pro", "Pro", 2900, 5000, 10240, 500, 5, "standard"),
    "enterprise": BillingPlan("enterprise", "Enterprise", 0, 100000, 102400, 10000, 100, "enterprise"),
}


def plan_manifest() -> list[dict]:
    return [plan.to_dict() for plan in DEFAULT_PLANS.values()]


def get_plan(plan_id: str) -> BillingPlan:
    if plan_id not in DEFAULT_PLANS:
        raise ValueError(f"unknown plan: {plan_id}")
    return DEFAULT_PLANS[plan_id]


def plan_policy(plan_id: str) -> dict:
    plan = get_plan(plan_id)
    return {
        "plan": plan.to_dict(),
        "requires_card": plan.id in {"pro", "enterprise"},
        "requires_contract": plan.id == "enterprise",
        "self_serve": plan.id in {"trial", "free", "pro"},
        "overage_enabled": plan.id in {"pro", "enterprise"},
    }
