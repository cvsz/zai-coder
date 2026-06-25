"""Quota enforcement middleware foundation."""

from __future__ import annotations

from dataclasses import dataclass

from zai_coder.monetization_core.plans import get_plan
from zai_coder.monetization_core.usage import UsageStore


RESOURCE_LIMIT_FIELDS = {
    "agent_run": "monthly_agent_runs",
    "media_job": "monthly_media_jobs",
    "api_request": "monthly_api_requests",
}


@dataclass(frozen=True)
class QuotaDecision:
    allowed: bool
    resource: str
    used: int
    limit: int
    reason: str

    def to_dict(self) -> dict:
        return {"allowed": self.allowed, "resource": self.resource, "used": self.used, "limit": self.limit, "reason": self.reason}


def check_quota(usage_store: UsageStore, account_id: str, plan_slug: str, resource: str, requested_units: int = 1) -> QuotaDecision:
    if requested_units <= 0:
        raise ValueError("requested_units must be positive")
    plan = get_plan(plan_slug)
    field = RESOURCE_LIMIT_FIELDS.get(resource)
    if not field:
        raise ValueError(f"unknown quota resource: {resource}")
    limit = int(getattr(plan, field))
    used = usage_store.total(account_id, resource)
    if used + requested_units > limit:
        return QuotaDecision(False, resource, used, limit, "quota-exceeded")
    return QuotaDecision(True, resource, used, limit, "allowed")
