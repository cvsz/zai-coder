"""Feature flag administration."""

from __future__ import annotations

from .models import FeatureFlag


DEFAULT_FLAGS = [
    FeatureFlag("gateway-v2", "Production API Gateway v2", True, "global", "platform", "Enable gateway UI/routes."),
    FeatureFlag("agent-marketplace", "Agent Marketplace", True, "org", "platform", "Enable local marketplace catalog."),
    FeatureFlag("self-healing", "Self-Healing Operations", False, "workspace", "ops", "Enable self-healing dashboard."),
    FeatureFlag("board-pack", "Board Pack Reporting", True, "org", "executive", "Enable board-pack reporting."),
]


def feature_flag_catalog() -> list[dict]:
    return [flag.to_dict() for flag in DEFAULT_FLAGS]


def feature_flag_validation_report() -> dict:
    reports = [{"id": flag.id, "issues": flag.validate()} for flag in DEFAULT_FLAGS]
    return {"ok": all(not item["issues"] for item in reports), "reports": reports}


def feature_flag_change_plan(flag_id: str, enabled: bool, scope_target: str = "global", approval_id: str = "") -> dict:
    match = next((flag for flag in DEFAULT_FLAGS if flag.id == flag_id), None)
    if not match:
        raise ValueError(f"unknown feature flag: {flag_id}")
    blocked = []
    if match.scope == "global" and not approval_id.startswith("approved_"):
        blocked.append("global feature flag changes require approval")
    return {
        "dry_run": True,
        "allowed": not blocked,
        "blocked": blocked,
        "flag": match.to_dict(),
        "change": {"enabled": enabled, "scope_target": scope_target},
    }
