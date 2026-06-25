"""Plan catalog for ZAI Coder monetization core.

All values are local metadata. This module does not contact payment providers.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict


@dataclass(frozen=True)
class Plan:
    slug: str
    name: str
    monthly_price_cents: int
    currency: str = "USD"
    max_members: int = 1
    max_workspaces: int = 1
    monthly_agent_runs: int = 100
    monthly_media_jobs: int = 20
    monthly_api_requests: int = 1000
    included_credit_units: int = 1000
    features: tuple[str, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict:
        return {
            "slug": self.slug,
            "name": self.name,
            "monthly_price_cents": self.monthly_price_cents,
            "currency": self.currency,
            "max_members": self.max_members,
            "max_workspaces": self.max_workspaces,
            "monthly_agent_runs": self.monthly_agent_runs,
            "monthly_media_jobs": self.monthly_media_jobs,
            "monthly_api_requests": self.monthly_api_requests,
            "included_credit_units": self.included_credit_units,
            "features": list(self.features),
        }


DEFAULT_PLANS: Dict[str, Plan] = {
    "free": Plan(
        slug="free",
        name="Free",
        monthly_price_cents=0,
        max_members=1,
        max_workspaces=1,
        monthly_agent_runs=50,
        monthly_media_jobs=5,
        monthly_api_requests=500,
        included_credit_units=500,
        features=("local_agent", "dry_run", "basic_media"),
    ),
    "builder": Plan(
        slug="builder",
        name="Builder",
        monthly_price_cents=1900,
        max_members=3,
        max_workspaces=5,
        monthly_agent_runs=1000,
        monthly_media_jobs=100,
        monthly_api_requests=20000,
        included_credit_units=10000,
        features=("local_agent", "creative_automation", "github_release", "audit_log"),
    ),
    "team": Plan(
        slug="team",
        name="Team",
        monthly_price_cents=4900,
        max_members=10,
        max_workspaces=25,
        monthly_agent_runs=5000,
        monthly_media_jobs=500,
        monthly_api_requests=100000,
        included_credit_units=50000,
        features=("members", "workspaces", "policy", "audit_dashboard", "priority_queue"),
    ),
    "enterprise": Plan(
        slug="enterprise",
        name="Enterprise",
        monthly_price_cents=19900,
        max_members=100,
        max_workspaces=250,
        monthly_agent_runs=50000,
        monthly_media_jobs=5000,
        monthly_api_requests=1000000,
        included_credit_units=500000,
        features=("sso_ready", "governance", "advanced_audit", "private_deploy", "custom_policy"),
    ),
}


def get_plan(slug: str) -> Plan:
    key = slug.strip().lower()
    if key not in DEFAULT_PLANS:
        raise ValueError(f"unknown plan: {slug}")
    return DEFAULT_PLANS[key]


def list_plans() -> list[dict]:
    return [plan.to_dict() for plan in DEFAULT_PLANS.values()]
