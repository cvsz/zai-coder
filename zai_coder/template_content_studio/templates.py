"""Template registry."""

from __future__ import annotations

from .models import ContentTemplate


DEFAULT_TEMPLATES = [
    ContentTemplate(
        "tpl-welcome-email",
        "Customer welcome email draft",
        "email",
        "Hi {{customer_name}},\n\nWelcome to {{product_name}}. Your onboarding workspace is {{workspace_name}}.\n\nNext step: {{next_step}}.\n\nNo action has been performed automatically.",
        ("customer_name", "product_name", "workspace_name", "next_step"),
        "customer",
        "email",
        "approved",
        "customer",
    ),
    ContentTemplate(
        "tpl-release-note",
        "Release note template",
        "release_note",
        "# {{version}} Release Notes\n\n## Highlights\n\n{{highlights}}\n\n## Safety\n\n{{safety_notes}}\n",
        ("version", "highlights", "safety_notes"),
        "customer",
        "markdown",
        "approved",
        "customer",
    ),
    ContentTemplate(
        "tpl-help-article",
        "Help article draft template",
        "help_article",
        "# {{title}}\n\n## Overview\n\n{{overview}}\n\n## Steps\n\n{{steps}}\n\n## Safety\n\n{{safety}}\n",
        ("title", "overview", "steps", "safety"),
        "customer",
        "markdown",
        "approved",
        "customer",
    ),
    ContentTemplate(
        "tpl-board-summary",
        "Board summary snippet",
        "document",
        "## {{period}} Executive Summary\n\n{{summary}}\n\n### Decisions Needed\n\n{{decisions}}\n",
        ("period", "summary", "decisions"),
        "investor",
        "document",
        "approved",
        "internal",
    ),
    ContentTemplate(
        "tpl-roadmap-update",
        "Roadmap update post draft",
        "document",
        "# Roadmap Update\n\nNow: {{now}}\n\nNext: {{next}}\n\nLater: {{later}}\n\nPrivate roadmap items are excluded from customer views.",
        ("now", "next", "later"),
        "customer",
        "portal",
        "approved",
        "customer",
    ),
]


def template_registry() -> list[dict]:
    return [template.to_dict() for template in DEFAULT_TEMPLATES]


def template_validation_report() -> dict:
    reports = [{"id": template.id, "issues": template.validate()} for template in DEFAULT_TEMPLATES]
    return {"ok": all(not item["issues"] for item in reports), "reports": reports}


def template_by_id(template_id: str) -> ContentTemplate:
    for template in DEFAULT_TEMPLATES:
        if template.id == template_id:
            return template
    raise ValueError(f"unknown template: {template_id}")


def templates_by_visibility(visibility: str = "customer") -> list[dict]:
    if visibility not in {"private", "customer", "public", "internal"}:
        raise ValueError("invalid visibility")
    if visibility == "private":
        return template_registry()
    allowed = {"public"} if visibility == "public" else {"customer", "public"}
    if visibility == "internal":
        allowed = {"customer", "public", "internal"}
    return [template.to_dict() for template in DEFAULT_TEMPLATES if template.visibility in allowed]
