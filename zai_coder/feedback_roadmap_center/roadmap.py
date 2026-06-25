"""Roadmap item registry."""

from __future__ import annotations

from .models import RoadmapItem


DEFAULT_ROADMAP = [
    RoadmapItem(
        "rm-connectors-prod",
        "Production connector enablement",
        "Promote plan-only connector adapters into approved provider-backed integrations.",
        "integrations",
        "candidate",
        "next",
        "private",
        "platform",
        ("fb_connector",),
    ),
    RoadmapItem(
        "rm-roadmap-public",
        "Customer-visible roadmap view",
        "Create a sanitized roadmap view for customers without private operational details.",
        "customer",
        "planned",
        "next",
        "customer",
        "product",
        ("fb_roadmap",),
    ),
    RoadmapItem(
        "rm-analytics-growth",
        "Usage analytics growth insights",
        "Connect analytics insights to onboarding and product backlog recommendations.",
        "growth",
        "planned",
        "now",
        "private",
        "growth",
        ("fb_analytics",),
    ),
    RoadmapItem(
        "rm-compliance-evidence",
        "Compliance evidence completion workflow",
        "Close compliance evidence gaps and prepare reviewable audit packages.",
        "compliance",
        "candidate",
        "later",
        "private",
        "compliance",
        ("fb_compliance",),
    ),
]


def roadmap_registry() -> list[dict]:
    return [item.to_dict() for item in DEFAULT_ROADMAP]


def roadmap_validation_report() -> dict:
    reports = [{"id": item.id, "issues": item.validate()} for item in DEFAULT_ROADMAP]
    return {"ok": all(not item["issues"] for item in reports), "reports": reports}


def roadmap_by_visibility(visibility: str = "customer") -> list[dict]:
    if visibility not in {"private", "customer", "public"}:
        raise ValueError("invalid visibility")
    if visibility == "private":
        return roadmap_registry()
    allowed = {"public"} if visibility == "public" else {"public", "customer"}
    return [item.to_dict() for item in DEFAULT_ROADMAP if item.visibility in allowed]


def roadmap_by_horizon(horizon: str = "next") -> list[dict]:
    if horizon not in {"now", "next", "later"}:
        raise ValueError("invalid horizon")
    return [item.to_dict() for item in DEFAULT_ROADMAP if item.horizon == horizon]
