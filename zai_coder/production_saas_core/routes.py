"""Production SaaS route registry."""

from __future__ import annotations

from zai_coder.monetization_core.plans import list_plans
from .dashboards import render_billing_dashboard, render_usage_dashboard, render_audit_dashboard, render_settings_dashboard
from .wizards.first_run import build_first_run_plan
from .wizards.deployment import build_deployment_plan


def route_saas_status() -> dict:
    return {
        "ok": True,
        "service": "zai-production-saas-core",
        "systems": [
            "organizations",
            "workspaces",
            "users",
            "invitations",
            "auth_enforcement",
            "quota_enforcement",
            "billing_dashboard",
            "usage_dashboard",
            "audit_dashboard",
            "settings_dashboard",
            "integration_audit",
            "deployment_wizard",
            "first_run_wizard",
        ],
    }


def route_billing_dashboard(subscriptions: list[dict] | None = None) -> dict:
    return {"content_type": "text/html", "html": render_billing_dashboard(list_plans(), subscriptions or [])}


def route_usage_dashboard(usage_rows: list[dict] | None = None, quota_rows: list[dict] | None = None) -> dict:
    return {"content_type": "text/html", "html": render_usage_dashboard(usage_rows or [], quota_rows or [])}


def route_audit_dashboard(events: list[dict] | None = None) -> dict:
    return {"content_type": "text/html", "html": render_audit_dashboard(events or [])}


def route_settings_dashboard(settings: dict | None = None) -> dict:
    return {"content_type": "text/html", "html": render_settings_dashboard(settings or {"mode": "local-first"})}


def route_first_run_plan(payload: dict) -> dict:
    return build_first_run_plan(payload.get("admin_email", "admin@example.com"), payload.get("org_slug", "default-org"), payload.get("workspace_slug", "default")).to_dict()


def route_deployment_plan(payload: dict) -> dict:
    return build_deployment_plan(payload.get("hostname", "zai.example.com"), payload.get("mode", "local-cloudflare")).to_dict()
