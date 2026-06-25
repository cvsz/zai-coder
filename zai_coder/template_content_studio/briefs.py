"""Content brief builder."""

from __future__ import annotations

import uuid

from .models import ContentBrief


def build_content_brief(
    title: str = "Customer onboarding welcome content",
    objective: str = "Help a new customer understand the next safe onboarding step.",
    audience: str = "customer",
    channel: str = "email",
    tone: str = "friendly",
    required_points: tuple[str, ...] = ("local-first", "review-first", "no automatic external publishing"),
) -> ContentBrief:
    brief = ContentBrief(
        id=f"brief_{uuid.uuid4().hex[:12]}",
        title=title,
        objective=objective,
        audience=audience,
        channel=channel,
        tone=tone,
        required_points=required_points,
    )
    issues = brief.validate()
    if issues:
        raise ValueError("; ".join(issues))
    return brief


def brief_to_template_variables(brief: dict) -> dict:
    return {
        "title": brief["title"],
        "overview": brief["objective"],
        "steps": "\n".join(f"- {point}" for point in brief.get("required_points", [])),
        "safety": "All content is local-first, review-first, and export-only by default.",
    }


def brief_validation_report() -> dict:
    demo = build_content_brief()
    return {"ok": not demo.validate(), "brief": demo.to_dict(), "issues": demo.validate()}
