"""Knowledge Base and Help Center control helpers."""

from __future__ import annotations

from .articles import article_registry, article_validation_report, article_by_visibility
from .faq import faq_catalog, faq_validation_report
from .search import help_search, search_validation_report
from .deflection import support_deflection_suggestions, deflection_policy
from .feedback_loop import HelpFeedbackStore, article_feedback_summary
from .exporter import write_help_export, write_help_report, help_export_bundle
from .audit import HelpAuditLog


def help_center_status() -> dict:
    return {
        "ok": True,
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


def help_center_overview() -> dict:
    return {
        "status": help_center_status(),
        "articles": article_registry(),
        "article_validation": article_validation_report(),
        "faqs": faq_catalog(),
        "faq_validation": faq_validation_report(),
        "search_demo": help_search("billing no charge"),
        "search_validation": search_validation_report(),
        "customer_view": article_by_visibility("customer"),
        "deflection_policy": deflection_policy(),
    }


def help_center_demo(db_path: str = "data/help-center.db", root: str = ".") -> dict:
    feedback_store = HelpFeedbackStore(db_path)
    feedback = feedback_store.submit("help-billing-draft", True, "This answered my billing question.", "cust_demo")
    suggestions = support_deflection_suggestions("Will this charge my card?", "billing")
    export_path = write_help_export(root, "customer")
    report_path = write_help_report(root, "customer")
    audit = HelpAuditLog(db_path).record("system", "help.export_generated", "help-center", {"export_path": export_path})
    return {
        "feedback": feedback.to_dict(),
        "feedback_summary": article_feedback_summary(feedback_store.list_feedback("help-billing-draft")),
        "suggestions": suggestions,
        "export_path": export_path,
        "report_path": report_path,
        "export_bundle": help_export_bundle("customer"),
        "audit": audit.to_dict(),
    }
