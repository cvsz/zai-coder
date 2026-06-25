"""Overage alerts and pricing."""

from __future__ import annotations

from .models import WorkspaceUsageSummary
from .plans import get_plan


OVERAGE_RATES_CENTS = {
    "run": 1,
    "storage_mb": 2,
    "provider_apply": 10,
}


def calculate_overage_cents(plan_id: str, usage: WorkspaceUsageSummary) -> dict:
    plan = get_plan(plan_id)
    over = {
        "run": max(0, usage.monthly_runs - plan.monthly_runs_limit),
        "storage_mb": max(0, usage.storage_mb - plan.storage_mb_limit),
        "provider_apply": max(0, usage.provider_apply - plan.provider_apply_limit),
    }
    charges = {key: quantity * OVERAGE_RATES_CENTS[key] for key, quantity in over.items()}
    return {"quantities": over, "charges_cents": charges, "total_cents": sum(charges.values())}


def overage_alerts(plan_id: str, usage: WorkspaceUsageSummary, warn_ratio: float = 0.8) -> list[dict]:
    plan = get_plan(plan_id)
    checks = [
        ("monthly_runs", usage.monthly_runs, plan.monthly_runs_limit),
        ("storage_mb", usage.storage_mb, plan.storage_mb_limit),
        ("provider_apply", usage.provider_apply, plan.provider_apply_limit),
    ]
    alerts = []
    for name, value, limit in checks:
        if limit == 0:
            continue
        ratio = value / limit
        if ratio >= warn_ratio:
            alerts.append({"metric": name, "value": value, "limit": limit, "ratio": ratio, "severity": "critical" if ratio >= 1 else "warning"})
    return alerts
