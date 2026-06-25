"""Notification template registry."""

from __future__ import annotations

from .models import NotificationTemplate


DEFAULT_TEMPLATES = [
    NotificationTemplate(
        "ntpl-welcome",
        "Portal welcome notice",
        "portal",
        "Welcome to {{product_name}}",
        "Hi {{customer_name}}, welcome to {{product_name}}. Your next step is: {{next_step}}. This notice is local-first and review-first.",
        ("customer_name", "product_name", "next_step"),
        "customer",
        "approved",
        "customer",
    ),
    NotificationTemplate(
        "ntpl-release",
        "Release update draft",
        "email",
        "{{version}} release update",
        "{{version}} is ready for review. Highlights: {{highlights}}. No external sending is performed automatically.",
        ("version", "highlights"),
        "customer",
        "approved",
        "customer",
    ),
    NotificationTemplate(
        "ntpl-roadmap",
        "Roadmap feedback reminder",
        "portal",
        "Roadmap feedback requested",
        "Please review the customer-visible roadmap update: {{roadmap_summary}}. Private roadmap items are excluded.",
        ("roadmap_summary",),
        "customer",
        "approved",
        "customer",
    ),
    NotificationTemplate(
        "ntpl-support",
        "Support follow-up draft",
        "portal",
        "Support follow-up",
        "Support ticket {{ticket_id}} is awaiting review. Suggested help article: {{help_article}}.",
        ("ticket_id", "help_article"),
        "support",
        "approved",
        "internal",
    ),
]


def notification_template_registry() -> list[dict]:
    return [template.to_dict() for template in DEFAULT_TEMPLATES]


def notification_template_validation_report() -> dict:
    reports = [{"id": template.id, "issues": template.validate()} for template in DEFAULT_TEMPLATES]
    return {"ok": all(not item["issues"] for item in reports), "reports": reports}


def notification_template_by_id(template_id: str) -> NotificationTemplate:
    for template in DEFAULT_TEMPLATES:
        if template.id == template_id:
            return template
    raise ValueError(f"unknown notification template: {template_id}")


def templates_by_channel(channel: str) -> list[dict]:
    return [template.to_dict() for template in DEFAULT_TEMPLATES if template.channel == channel]
