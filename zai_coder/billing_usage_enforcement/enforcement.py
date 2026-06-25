"""Quota-to-plan enforcement."""

from __future__ import annotations

from .models import WorkspaceUsageSummary
from .plans import get_plan


def enforce_plan_limits(plan_id: str, usage: WorkspaceUsageSummary) -> dict:
    plan = get_plan(plan_id)
    checks = {
        "monthly_runs": usage.monthly_runs <= plan.monthly_runs_limit,
        "storage_mb": usage.storage_mb <= plan.storage_mb_limit,
        "provider_apply": usage.provider_apply <= plan.provider_apply_limit,
        "seats": usage.seats <= plan.seats_limit,
    }
    blocked = [name for name, ok in checks.items() if not ok]
    return {
        "allowed": not blocked,
        "blocked": blocked,
        "checks": checks,
        "plan": plan.to_dict(),
        "usage": usage.to_dict(),
    }


def action_enforcement_decision(plan_id: str, usage: WorkspaceUsageSummary, action: str) -> dict:
    limits = enforce_plan_limits(plan_id, usage)
    if not limits["allowed"]:
        return {"allowed": False, "reason": "plan limit exceeded", **limits}
    if action == "provider_apply" and usage.provider_apply >= limits["plan"]["provider_apply_limit"]:
        return {"allowed": False, "reason": "provider apply quota exhausted", **limits}
    return {"allowed": True, "reason": "allowed", **limits}
