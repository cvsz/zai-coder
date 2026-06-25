"""Template and Content Studio control helpers."""

from __future__ import annotations

from .templates import template_registry, template_validation_report, templates_by_visibility
from .variables import validate_template_variables
from .briefs import build_content_brief, brief_to_template_variables, brief_validation_report
from .render import render_template, render_demo_content
from .brand import brand_rules, content_safety_gate
from .approvals import create_approval, approval_decision, approval_policy
from .library import content_library_bundle, write_content_library_export
from .exporter import write_rendered_content, write_content_studio_export, write_content_report
from .faq_bridge import suggested_template_for_intent
from .audit import ContentAuditLog


def content_studio_status() -> dict:
    return {
        "ok": True,
        "systems": [
            "content_template_registry",
            "variable_schema_validation",
            "safe_local_render_engine",
            "brand_tone_rules",
            "content_brief_builder",
            "approval_workflow",
            "content_library_export",
            "help_center_template_bridge",
            "template_content_dashboard",
            "content_audit_log",
        ],
    }


def content_studio_overview() -> dict:
    templates = template_registry()
    return {
        "status": content_studio_status(),
        "templates": templates,
        "template_validation": template_validation_report(),
        "variable_validation": [validate_template_variables(template) for template in templates],
        "customer_templates": templates_by_visibility("customer"),
        "brand_rules": brand_rules(),
        "brief_validation": brief_validation_report(),
        "approval_policy": approval_policy(),
    }


def content_studio_demo(root: str = ".", db_path: str = "data/template-content-studio.db") -> dict:
    brief = build_content_brief()
    rendered = render_template("tpl-help-article", brief_to_template_variables(brief.to_dict()))
    safety = content_safety_gate(rendered.to_dict())
    approval = create_approval(rendered.id)
    approval_review = approval_decision(approval.to_dict(), "approved", "owner", "Reviewed locally.")
    rendered_paths = write_rendered_content(rendered.to_dict(), root)
    library_path = write_content_library_export(root, "customer")
    export_path = write_content_studio_export(root)
    report_path = write_content_report(root)
    audit = ContentAuditLog(db_path).record("system", "content.rendered", rendered.id, {"export_path": export_path})
    return {
        "brief": brief.to_dict(),
        "rendered": rendered.to_dict(),
        "safety": safety,
        "approval": approval_review,
        "rendered_paths": rendered_paths,
        "library_path": library_path,
        "export_path": export_path,
        "report_path": report_path,
        "suggested_template": suggested_template_for_intent("help article"),
        "audit": audit.to_dict(),
    }
