"""FAQ catalog."""

from __future__ import annotations

from .models import FAQItem


DEFAULT_FAQ = [
    FAQItem("faq-no-charge", "Will this charge my card?", "No. Billing flows are draft-only and payment capture is disabled.", "billing", "customer", "help-billing-draft"),
    FAQItem("faq-onboarding", "How do I start onboarding?", "Open the onboarding checklist and complete workspace, security, billing, support, and go-live review steps.", "onboarding", "customer", "help-getting-started"),
    FAQItem("faq-connectors", "Can connectors call GitHub or other providers?", "Not by default. Connector setup is plan-first unless approved provider adapters are added later.", "integrations", "customer", "help-connectors"),
    FAQItem("faq-roadmap-private", "Can customers see private roadmap items?", "No. Customer views exclude private roadmap items.", "roadmap", "customer", "help-roadmap"),
]


def faq_catalog() -> list[dict]:
    return [item.to_dict() for item in DEFAULT_FAQ]


def faq_validation_report() -> dict:
    reports = [{"id": item.id, "issues": item.validate()} for item in DEFAULT_FAQ]
    return {"ok": all(not item["issues"] for item in reports), "reports": reports}


def faq_by_category(category: str) -> list[dict]:
    return [item.to_dict() for item in DEFAULT_FAQ if item.category == category]
