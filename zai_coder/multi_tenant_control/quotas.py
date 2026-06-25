"""Workspace quota enforcement."""

from __future__ import annotations

from .models import WorkspaceQuota


def quota_decision(quota: WorkspaceQuota, usage: dict[str, int]) -> dict:
    checks = {
        "monthly_runs": usage.get("monthly_runs", 0) <= quota.monthly_runs_limit,
        "storage_mb": usage.get("storage_mb", 0) <= quota.storage_mb_limit,
        "provider_apply": usage.get("provider_apply", 0) <= quota.provider_apply_limit,
    }
    blocked = [name for name, ok in checks.items() if not ok]
    return {
        "allowed": not blocked,
        "blocked": blocked,
        "checks": checks,
        "quota": quota.to_dict(),
        "usage": dict(usage),
    }


def default_usage() -> dict[str, int]:
    return {"monthly_runs": 0, "storage_mb": 0, "provider_apply": 0}
