"""Final App Studio route registry."""

from __future__ import annotations

from zai_coder.app_studio_final.ui.pages import render_home_page, render_plugins_page, render_workflows_page, render_models_page, render_deployments_page
from zai_coder.app_studio_final.plugin_marketplace import list_plugins
from zai_coder.app_studio_final.workflow_builder import default_release_workflow
from zai_coder.app_studio_final.model_router_ui import list_model_routes
from zai_coder.app_studio_final.deployment_control import default_deployment_targets
from zai_coder.app_studio_final.wizards.app_generator import generate_app_plan
from zai_coder.app_studio_final.audit_search import search_audit_events


def route_final_status() -> dict:
    return {
        "ok": True,
        "service": "zai-app-studio-final",
        "systems": [
            "admin_ui_shell",
            "plugin_marketplace",
            "app_generator",
            "workflow_builder",
            "model_router_ui",
            "deployment_control_center",
            "api_key_ui",
            "audit_search",
            "approval_queue",
            "project_archive",
        ],
    }


def route_home() -> dict:
    return {"content_type": "text/html", "html": render_home_page()}


def route_plugins() -> dict:
    return {"content_type": "text/html", "html": render_plugins_page(list_plugins())}


def route_workflows() -> dict:
    wf = default_release_workflow()
    return {"content_type": "text/html", "html": render_workflows_page([{"name": wf.name, "status": wf.status, "steps": [s.name for s in wf.steps]}])}


def route_models() -> dict:
    return {"content_type": "text/html", "html": render_models_page(list_model_routes())}


def route_deployments() -> dict:
    return {"content_type": "text/html", "html": render_deployments_page(default_deployment_targets())}


def route_app_generator(payload: dict) -> dict:
    return generate_app_plan(payload.get("app_name", "Demo App"), payload.get("app_type", "web")).to_dict()


def route_audit_search(payload: dict) -> dict:
    return {"results": search_audit_events(payload.get("events", []), payload.get("query", ""), payload.get("actor", ""), payload.get("action", ""))}
