"""Template and Content Studio route registry."""

from __future__ import annotations

from zai_coder.template_content_studio.control import content_studio_status, content_studio_overview, content_studio_demo
from zai_coder.template_content_studio.templates import template_registry, template_validation_report, templates_by_visibility
from zai_coder.template_content_studio.variables import validate_template_variables, validate_render_variables, extract_variables
from zai_coder.template_content_studio.render import render_demo_content
from zai_coder.template_content_studio.briefs import build_content_brief, brief_to_template_variables
from zai_coder.template_content_studio.brand import brand_rules, content_safety_gate, tone_guard
from zai_coder.template_content_studio.approvals import approval_policy, create_approval, approval_decision
from zai_coder.template_content_studio.library import content_library_bundle, write_content_library_export
from zai_coder.template_content_studio.exporter import write_content_studio_export, write_content_report
from zai_coder.template_content_studio.faq_bridge import suggested_template_for_intent
from zai_coder.template_content_studio.audit import ContentAuditLog
from zai_coder.template_content_studio.ui.pages import render_content_overview_page, render_templates_page, render_render_page, render_brand_page, render_library_page


def route_content_studio_status() -> dict:
    return {
        "ok": True,
        "service": "zai-template-and-content-studio",
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


def route_content_studio_overview() -> dict:
    return content_studio_overview()


def route_content_templates() -> dict:
    templates = template_registry()
    return {"templates": templates, "customer": templates_by_visibility("customer"), "validation": template_validation_report()}


def route_template_variables() -> dict:
    template = template_registry()[0]
    return {"variables": extract_variables(template["body"]), "validation": validate_template_variables(template)}


def route_render_demo() -> dict:
    return render_demo_content()


def route_content_brief() -> dict:
    brief = build_content_brief()
    return {"brief": brief.to_dict(), "template_variables": brief_to_template_variables(brief.to_dict())}


def route_brand_rules() -> dict:
    demo = render_demo_content()["rendered"]
    return {"brand": brand_rules(), "tone": tone_guard(demo["content"]), "safety": content_safety_gate(demo)}


def route_content_approval() -> dict:
    rendered = render_demo_content()["rendered"]
    approval = create_approval(rendered["id"])
    return {"policy": approval_policy(), "approval": approval.to_dict(), "decision": approval_decision(approval.to_dict(), "approved", "owner")}


def route_content_library() -> dict:
    return {"bundle": content_library_bundle("customer"), "path": write_content_library_export(".", "customer")}


def route_content_export() -> dict:
    return {"export_path": write_content_studio_export("."), "report_path": write_content_report(".")}


def route_content_suggest_template() -> dict:
    return suggested_template_for_intent("help article")


def route_content_demo() -> dict:
    return content_studio_demo(".", "data/template-content-studio-demo.db")


def route_content_audit() -> dict:
    return {"events": ContentAuditLog().list_events()}


def route_content_studio_page() -> dict:
    return {"content_type": "text/html", "html": render_content_overview_page()}


def route_content_templates_page() -> dict:
    return {"content_type": "text/html", "html": render_templates_page()}


def route_content_render_page() -> dict:
    return {"content_type": "text/html", "html": render_render_page()}


def route_content_brand_page() -> dict:
    return {"content_type": "text/html", "html": render_brand_page()}


def route_content_library_page() -> dict:
    return {"content_type": "text/html", "html": render_library_page()}
