from pathlib import Path

from zai_coder.knowledge_base_help_center.models import HelpArticle, FAQItem, SearchResult, HelpFeedback
from zai_coder.knowledge_base_help_center.articles import article_registry, article_validation_report, article_by_visibility, article_by_id
from zai_coder.knowledge_base_help_center.faq import faq_catalog, faq_validation_report, faq_by_category
from zai_coder.knowledge_base_help_center.search import tokenize, score_text, help_search, search_validation_report
from zai_coder.knowledge_base_help_center.deflection import support_deflection_suggestions, deflection_policy
from zai_coder.knowledge_base_help_center.feedback_loop import HelpFeedbackStore, article_feedback_summary
from zai_coder.knowledge_base_help_center.exporter import help_export_bundle, write_help_export, help_report_markdown, write_help_report
from zai_coder.knowledge_base_help_center.audit import HelpAuditLog
from zai_coder.knowledge_base_help_center.control import help_center_status, help_center_overview, help_center_demo
from zai_coder.knowledge_base_help_center.ui.pages import render_help_overview_page, render_articles_page, render_faq_page, render_search_page, render_admin_help_page
from zai_coder.knowledge_base_help_center.routes import (
    route_help_center_status,
    route_help_center_overview,
    route_help_articles,
    route_help_article,
    route_help_faq,
    route_help_search,
    route_help_deflection,
    route_help_feedback_demo,
    route_help_export,
    route_help_report,
    route_help_demo,
    route_help_audit,
    route_help_page,
    route_help_articles_page,
    route_help_faq_page,
    route_help_search_page,
    route_help_admin_page,
)


def test_models_validation():
    assert HelpArticle("a", "Title", "Body").validate() == []
    assert HelpArticle("", "", "token", category="bad", audience="bad", status="bad", visibility="bad").validate()
    assert FAQItem("f", "Question?", "Answer").validate() == []
    assert FAQItem("", "No question", "", visibility="bad").validate()
    assert SearchResult("s", "Title", 1).validate() == []
    assert SearchResult("", "", -1, kind="bad").validate()
    assert HelpFeedback("h", "a", True).validate() == []
    assert HelpFeedback("", "", True, "secret here").validate()


def test_articles_faq_search_deflection():
    assert article_registry()
    assert article_validation_report()["ok"] is True
    assert article_by_id("help-getting-started")["id"] == "help-getting-started"
    assert all(item["visibility"] in {"customer", "public"} for item in article_by_visibility("customer"))
    assert faq_catalog()
    assert faq_validation_report()["ok"] is True
    assert faq_by_category("billing")
    assert "billing" in tokenize("Billing, charge?")
    assert score_text("billing charge", "billing no charge") >= 2
    search = help_search("billing charge")
    assert search["results"]
    assert search_validation_report()["ok"] is True
    suggestions = support_deflection_suggestions("Will this charge my card?", "billing")
    assert suggestions["send_external_message"] is False
    assert deflection_policy()["no_auto_reply"] is True


def test_feedback_export_audit(tmp_path):
    store = HelpFeedbackStore(tmp_path / "help.db")
    item = store.submit("help-billing-draft", True, "Helpful", "cust_demo")
    assert store.list_feedback("help-billing-draft")[0]["id"] == item.id
    assert article_feedback_summary(store.list_feedback())["helpful_rate"] == 1.0
    bundle = help_export_bundle("customer")
    assert bundle["external_publish"] is False
    export_path = write_help_export(tmp_path, "customer")
    report_path = write_help_report(tmp_path, "customer")
    assert Path(export_path).exists()
    assert Path(report_path).exists()
    assert "Knowledge Base" in help_report_markdown("customer")
    audit = HelpAuditLog(tmp_path / "help.db")
    event = audit.record("tester", "help.test", "target")
    assert audit.list_events()[0]["id"] == event.id


def test_control_ui_routes(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert help_center_status()["ok"] is True
    overview = help_center_overview()
    assert overview["status"]["ok"] is True
    demo = help_center_demo(str(tmp_path / "demo.db"), str(tmp_path))
    assert Path(demo["export_path"]).exists()
    assert Path(demo["report_path"]).exists()
    assert "Knowledge Base and Help Center" in render_help_overview_page()
    assert "Articles" in render_articles_page()
    assert "FAQ" in render_faq_page()
    assert "Search" in render_search_page()
    assert "Admin View" in render_admin_help_page()
    assert route_help_center_status()["ok"] is True
    assert route_help_center_overview()["status"]["ok"] is True
    assert route_help_articles()["validation"]["ok"] is True
    assert route_help_article()["id"] == "help-getting-started"
    assert route_help_faq()["validation"]["ok"] is True
    assert route_help_search()["search"]["results"]
    assert route_help_deflection()["suggestions"]["auto_reply"] is False
    assert route_help_feedback_demo()["summary"]["total"] == 1
    assert Path(route_help_export()["path"]).exists()
    assert Path(route_help_report()["path"]).exists()
    assert Path(route_help_demo()["export_path"]).exists()
    assert "events" in route_help_audit()
    assert route_help_page()["content_type"] == "text/html"
    assert route_help_articles_page()["content_type"] == "text/html"
    assert route_help_faq_page()["content_type"] == "text/html"
    assert route_help_search_page()["content_type"] == "text/html"
    assert route_help_admin_page()["content_type"] == "text/html"


def test_docs_scripts_assets_exist():
    root = Path(__file__).resolve().parents[1]
    for rel in [
        "scripts/help-center/help-status.sh",
        "scripts/help-center/help-articles.sh",
        "scripts/help-center/help-faq.sh",
        "scripts/help-center/help-search.sh",
        "scripts/help-center/help-deflection.sh",
        "scripts/help-center/help-feedback-demo.sh",
        "scripts/help-center/help-demo.sh",
        "scripts/help-center/help-export.sh",
        "scripts/help-center/help-report.sh",
        "scripts/help-center/help-audit.sh",
        "scripts/help-center/help-dashboard-export.sh",
        "docs/help-center/KNOWLEDGE_BASE_HELP_CENTER_GUIDE.md",
        "docs/help-center/ARTICLE_REGISTRY.md",
        "docs/help-center/FAQ_CATALOG.md",
        "docs/help-center/HELP_SEARCH.md",
        "docs/help-center/SUPPORT_DEFLECTION.md",
        "docs/help-center/HELP_EXPORT_POLICY.md",
        "docs/requirements/NEXT_V37_KNOWLEDGE_BASE_HELP_CENTER_REQUIREMENTS.md",
        "assets/help-center/knowledge_base_help_center_features.json",
    ]:
        assert (root / rel).exists(), rel
