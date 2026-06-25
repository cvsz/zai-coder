"""Knowledge Base and Help Center route registry."""

from __future__ import annotations

from zai_coder.knowledge_base_help_center.control import help_center_status, help_center_overview, help_center_demo
from zai_coder.knowledge_base_help_center.articles import article_registry, article_by_visibility, article_validation_report, article_by_id
from zai_coder.knowledge_base_help_center.faq import faq_catalog, faq_validation_report, faq_by_category
from zai_coder.knowledge_base_help_center.search import help_search, search_validation_report
from zai_coder.knowledge_base_help_center.deflection import support_deflection_suggestions, deflection_policy
from zai_coder.knowledge_base_help_center.feedback_loop import HelpFeedbackStore, article_feedback_summary
from zai_coder.knowledge_base_help_center.exporter import help_export_bundle, write_help_export, help_report_markdown, write_help_report
from zai_coder.knowledge_base_help_center.audit import HelpAuditLog
from zai_coder.knowledge_base_help_center.ui.pages import render_help_overview_page, render_articles_page, render_faq_page, render_search_page, render_admin_help_page


def route_help_center_status() -> dict:
    return {
        "ok": True,
        "service": "zai-knowledge-base-and-help-center",
        "systems": [
            "help_article_registry",
            "faq_catalog",
            "local_help_search",
            "support_deflection_suggestions",
            "article_feedback_loop",
            "customer_admin_help_views",
            "safe_help_export_bundle",
            "help_center_dashboard",
            "help_audit_log",
        ],
    }


def route_help_center_overview() -> dict:
    return help_center_overview()


def route_help_articles() -> dict:
    return {"articles": article_registry(), "customer": article_by_visibility("customer"), "validation": article_validation_report()}


def route_help_article(article_id: str = "help-getting-started") -> dict:
    return article_by_id(article_id)


def route_help_faq() -> dict:
    return {"faqs": faq_catalog(), "billing": faq_by_category("billing"), "validation": faq_validation_report()}


def route_help_search(query: str = "billing charge") -> dict:
    return {"search": help_search(query), "validation": search_validation_report()}


def route_help_deflection() -> dict:
    return {"suggestions": support_deflection_suggestions("Will this charge my card?", "billing question"), "policy": deflection_policy()}


def route_help_feedback_demo() -> dict:
    store = HelpFeedbackStore("data/help-center-feedback-demo.db")
    item = store.submit("help-getting-started", True, "Helpful setup guide.", "cust_demo")
    return {"feedback": item.to_dict(), "summary": article_feedback_summary(store.list_feedback("help-getting-started"))}


def route_help_export() -> dict:
    return {"bundle": help_export_bundle("customer"), "path": write_help_export(".", "customer")}


def route_help_report() -> dict:
    return {"markdown": help_report_markdown("customer"), "path": write_help_report(".", "customer")}


def route_help_demo() -> dict:
    return help_center_demo("data/help-center-demo.db", ".")


def route_help_audit() -> dict:
    return {"events": HelpAuditLog().list_events()}


def route_help_page() -> dict:
    return {"content_type": "text/html", "html": render_help_overview_page()}


def route_help_articles_page() -> dict:
    return {"content_type": "text/html", "html": render_articles_page()}


def route_help_faq_page() -> dict:
    return {"content_type": "text/html", "html": render_faq_page()}


def route_help_search_page() -> dict:
    return {"content_type": "text/html", "html": render_search_page()}


def route_help_admin_page() -> dict:
    return {"content_type": "text/html", "html": render_admin_help_page()}
