from pathlib import Path

from zai_coder.template_content_studio.models import ContentTemplate, ContentBrief, RenderedContent, ContentApproval
from zai_coder.template_content_studio.templates import template_registry, template_validation_report, template_by_id, templates_by_visibility
from zai_coder.template_content_studio.variables import extract_variables, validate_template_variables, validate_render_variables
from zai_coder.template_content_studio.brand import brand_rules, tone_guard, content_safety_gate
from zai_coder.template_content_studio.render import render_template, render_html_preview, render_demo_content
from zai_coder.template_content_studio.briefs import build_content_brief, brief_to_template_variables, brief_validation_report
from zai_coder.template_content_studio.approvals import create_approval, approval_decision, approval_policy
from zai_coder.template_content_studio.faq_bridge import help_article_template_map, suggested_template_for_intent
from zai_coder.template_content_studio.library import content_library_bundle, write_content_library_export
from zai_coder.template_content_studio.exporter import write_rendered_content, content_studio_export_bundle, write_content_studio_export, write_content_report
from zai_coder.template_content_studio.audit import ContentAuditLog
from zai_coder.template_content_studio.control import content_studio_status, content_studio_overview, content_studio_demo
from zai_coder.template_content_studio.ui.pages import render_content_overview_page, render_templates_page, render_render_page, render_brand_page, render_library_page
from zai_coder.template_content_studio.routes import (
    route_content_studio_status,
    route_content_studio_overview,
    route_content_templates,
    route_template_variables,
    route_render_demo,
    route_content_brief,
    route_brand_rules,
    route_content_approval,
    route_content_library,
    route_content_export,
    route_content_suggest_template,
    route_content_demo,
    route_content_audit,
    route_content_studio_page,
    route_content_templates_page,
    route_content_render_page,
    route_content_brand_page,
    route_content_library_page,
)


def test_models_validation():
    assert ContentTemplate("t", "Title", "document", "Body").validate() == []
    assert ContentTemplate("", "", "bad", "token", audience="bad", channel="bad", status="bad", visibility="bad").validate()
    assert ContentBrief("b", "Brief", "Objective", "customer", "email").validate() == []
    assert ContentBrief("", "", "", "bad", "bad", tone="bad", status="bad").validate()
    assert RenderedContent("r", "t", "Title", "Body", "markdown").validate() == []
    assert RenderedContent("", "", "", "secret", "markdown", dry_run=False).validate()
    assert ContentApproval("a", "r").validate() == []
    assert ContentApproval("", "", status="bad").validate()


def test_templates_variables_brand_rendering():
    templates = template_registry()
    assert templates
    assert template_validation_report()["ok"] is True
    assert template_by_id("tpl-welcome-email").id == "tpl-welcome-email"
    assert templates_by_visibility("customer")
    variables = extract_variables("Hi {{name}}, welcome to {{ product }}")
    assert variables == ["name", "product"]
    tpl = template_by_id("tpl-welcome-email").to_dict()
    assert validate_template_variables(tpl)["ok"] is True
    good_vars = {"customer_name": "Demo", "product_name": "ZAI Coder Control Plane", "workspace_name": "WS", "next_step": "review local-first checklist"}
    assert validate_render_variables(tpl, good_vars)["ok"] is True
    assert validate_render_variables(tpl, {"customer_name": "Demo"})["ok"] is False
    assert brand_rules()["external_publish"] is False
    rendered = render_template("tpl-welcome-email", good_vars)
    assert rendered.dry_run is True
    assert "Demo" in rendered.content
    assert "article" in render_html_preview(rendered)
    assert content_safety_gate(rendered.to_dict())["allowed"] is True
    assert tone_guard("guaranteed compliance", "customer")["allowed"] is False
    assert route_render_demo()["safety"]["allowed"] is True


def test_briefs_approvals_library_exports_audit(tmp_path):
    brief = build_content_brief()
    assert brief.validate() == []
    variables = brief_to_template_variables(brief.to_dict())
    assert "local-first" in variables["steps"]
    assert brief_validation_report()["ok"] is True
    rendered = render_template("tpl-help-article", variables)
    approval = create_approval(rendered.id)
    decision = approval_decision(approval.to_dict(), "approved", "owner", "ok")
    assert decision["allowed"] is True
    assert approval_policy()["publish_disabled"] is True
    assert help_article_template_map()["help_article_template"] == "tpl-help-article"
    assert suggested_template_for_intent("release notes")["template_id"] == "tpl-release-note"
    bundle = content_library_bundle("customer")
    assert bundle["external_publish"] is False
    library_path = write_content_library_export(tmp_path, "customer")
    assert Path(library_path).exists()
    paths = write_rendered_content(rendered.to_dict(), tmp_path)
    assert Path(paths["json"]).exists()
    assert Path(paths["markdown"]).exists()
    export_path = write_content_studio_export(tmp_path)
    report_path = write_content_report(tmp_path)
    assert Path(export_path).exists()
    assert Path(report_path).exists()
    audit = ContentAuditLog(tmp_path / "content.db")
    event = audit.record("tester", "content.test", rendered.id)
    assert audit.list_events()[0]["id"] == event.id


def test_control_ui_routes(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert content_studio_status()["ok"] is True
    overview = content_studio_overview()
    assert overview["status"]["ok"] is True
    demo = content_studio_demo(str(tmp_path), str(tmp_path / "content.db"))
    assert Path(demo["export_path"]).exists()
    assert Path(demo["report_path"]).exists()
    assert "Template and Content Studio" in render_content_overview_page()
    assert "Templates" in render_templates_page()
    assert "Render Demo" in render_render_page()
    assert "Brand Rules" in render_brand_page()
    assert "Library" in render_library_page()
    assert route_content_studio_status()["ok"] is True
    assert route_content_studio_overview()["status"]["ok"] is True
    assert route_content_templates()["validation"]["ok"] is True
    assert route_template_variables()["validation"]["ok"] is True
    assert route_content_brief()["brief"]["id"].startswith("brief_")
    assert route_brand_rules()["safety"]["allowed"] is True
    assert route_content_approval()["decision"]["allowed"] is True
    assert Path(route_content_library()["path"]).exists()
    assert Path(route_content_export()["export_path"]).exists()
    assert route_content_suggest_template()["template_id"] == "tpl-help-article"
    assert Path(route_content_demo()["export_path"]).exists()
    assert "events" in route_content_audit()
    assert route_content_studio_page()["content_type"] == "text/html"
    assert route_content_templates_page()["content_type"] == "text/html"
    assert route_content_render_page()["content_type"] == "text/html"
    assert route_content_brand_page()["content_type"] == "text/html"
    assert route_content_library_page()["content_type"] == "text/html"


def test_docs_scripts_assets_exist():
    root = Path(__file__).resolve().parents[1]
    for rel in [
        "scripts/content-studio/content-status.sh",
        "scripts/content-studio/content-templates.sh",
        "scripts/content-studio/template-variables.sh",
        "scripts/content-studio/render-demo.sh",
        "scripts/content-studio/content-brief.sh",
        "scripts/content-studio/brand-rules.sh",
        "scripts/content-studio/content-approval.sh",
        "scripts/content-studio/content-library.sh",
        "scripts/content-studio/content-export.sh",
        "scripts/content-studio/content-demo.sh",
        "scripts/content-studio/content-audit.sh",
        "scripts/content-studio/content-dashboard-export.sh",
        "docs/content-studio/TEMPLATE_CONTENT_STUDIO_GUIDE.md",
        "docs/content-studio/TEMPLATE_REGISTRY.md",
        "docs/content-studio/VARIABLE_RENDERING.md",
        "docs/content-studio/BRAND_TONE_RULES.md",
        "docs/content-studio/CONTENT_APPROVAL.md",
        "docs/content-studio/CONTENT_EXPORT_POLICY.md",
        "docs/requirements/NEXT_V38_TEMPLATE_CONTENT_STUDIO_REQUIREMENTS.md",
        "assets/content-studio/template_content_studio_features.json",
    ]:
        assert (root / rel).exists(), rel
