"""Help article registry."""

from __future__ import annotations

from .models import HelpArticle


DEFAULT_ARTICLES = [
    HelpArticle(
        "help-getting-started",
        "Getting started with ZAI Coder Control Plane",
        "Use the customer portal onboarding checklist to review workspace, security, billing, support, and go-live steps.",
        "onboarding",
        "customer",
        "published",
        ("start", "onboarding", "portal"),
        "customer",
    ),
    HelpArticle(
        "help-billing-draft",
        "Understanding draft-only billing",
        "Billing handoff plans are local drafts. No real charge is created by the customer portal package.",
        "billing",
        "customer",
        "published",
        ("billing", "sandbox", "no-real-charge"),
        "customer",
    ),
    HelpArticle(
        "help-connectors",
        "Connector setup overview",
        "Connector setup remains plan-first. Provider calls are disabled unless an approved adapter and execution flow are added later.",
        "integrations",
        "customer",
        "published",
        ("connector", "integration", "github"),
        "customer",
    ),
    HelpArticle(
        "help-admin-service-actions",
        "Admin service action plans",
        "Admin service controls are dry-run plans. Healthcheck and status are read-only; restart, backup, drain, and rollback need approval.",
        "admin",
        "admin",
        "published",
        ("admin", "service", "dry-run"),
        "internal",
    ),
    HelpArticle(
        "help-roadmap",
        "Customer roadmap view",
        "Customer roadmap exports include customer and public items only. Private roadmap details stay internal.",
        "roadmap",
        "customer",
        "published",
        ("roadmap", "feedback", "visibility"),
        "customer",
    ),
]


def article_registry() -> list[dict]:
    return [article.to_dict() for article in DEFAULT_ARTICLES]


def article_validation_report() -> dict:
    reports = [{"id": article.id, "issues": article.validate()} for article in DEFAULT_ARTICLES]
    return {"ok": all(not item["issues"] for item in reports), "reports": reports}


def article_by_visibility(visibility: str = "customer") -> list[dict]:
    if visibility not in {"private", "customer", "public", "internal"}:
        raise ValueError("invalid visibility")
    if visibility == "private":
        return article_registry()
    allowed = {"public"} if visibility == "public" else {"public", "customer"}
    if visibility == "internal":
        allowed = {"public", "customer", "internal"}
    return [article.to_dict() for article in DEFAULT_ARTICLES if article.visibility in allowed]


def article_by_id(article_id: str) -> dict:
    for article in DEFAULT_ARTICLES:
        if article.id == article_id:
            return article.to_dict()
    raise ValueError(f"unknown article: {article_id}")
