"""Customer portal feature access."""

from __future__ import annotations

from .models import PortalFeature


PLAN_ORDER = {"free": 0, "pro": 1, "enterprise": 2, "internal": 3}

DEFAULT_FEATURES = [
    PortalFeature("dashboard", "Customer Dashboard", "free", True, "portal", "Customer home and status."),
    PortalFeature("onboarding", "Onboarding Wizard", "free", True, "onboarding", "Guided setup checklist."),
    PortalFeature("billing-summary", "Billing Summary", "free", True, "billing", "Draft-only billing summary."),
    PortalFeature("support", "Support Tickets", "free", True, "support", "Local support ticket flow."),
    PortalFeature("connectors", "Connector Setup", "pro", True, "integrations", "Plan connector setup."),
    PortalFeature("compliance-pack", "Compliance Pack", "enterprise", True, "compliance", "Readiness package exports."),
    PortalFeature("board-pack", "Board Pack", "enterprise", True, "reporting", "Board reporting exports."),
]


def feature_catalog() -> list[dict]:
    return [feature.to_dict() for feature in DEFAULT_FEATURES]


def feature_validation_report() -> dict:
    reports = [{"id": feature.id, "issues": feature.validate()} for feature in DEFAULT_FEATURES]
    return {"ok": all(not item["issues"] for item in reports), "reports": reports}


def feature_access(plan: str, feature_id: str) -> dict:
    feature = next((item for item in DEFAULT_FEATURES if item.id == feature_id), None)
    if not feature:
        raise ValueError(f"unknown feature: {feature_id}")
    allowed = feature.enabled and PLAN_ORDER[plan] >= PLAN_ORDER[feature.required_plan]
    return {
        "allowed": allowed,
        "plan": plan,
        "feature": feature.to_dict(),
        "reason": "feature available" if allowed else f"requires {feature.required_plan} plan",
    }


def customer_feature_matrix(plan: str) -> dict:
    return {"plan": plan, "features": [feature_access(plan, feature.id) for feature in DEFAULT_FEATURES]}
