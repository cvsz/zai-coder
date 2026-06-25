"""Customer Portal and Onboarding route registry."""

from __future__ import annotations

from zai_coder.customer_portal_onboarding.control import customer_portal_status, customer_overview, onboarding_demo, support_demo, customer_action_demo
from zai_coder.customer_portal_onboarding.accounts import customer_directory, customer_validation_report, create_customer_plan
from zai_coder.customer_portal_onboarding.features import feature_catalog, customer_feature_matrix, feature_access, feature_validation_report
from zai_coder.customer_portal_onboarding.onboarding import onboarding_steps, build_onboarding_plan, onboarding_progress, onboarding_step_validation_report
from zai_coder.customer_portal_onboarding.workspace_setup import workspace_setup_plan, workspace_setup_gate
from zai_coder.customer_portal_onboarding.billing_handoff import billing_handoff_draft, upgrade_request_plan
from zai_coder.customer_portal_onboarding.support import support_policy
from zai_coder.customer_portal_onboarding.exporter import customer_export_bundle, write_customer_export
from zai_coder.customer_portal_onboarding.audit import CustomerAuditLog
from zai_coder.customer_portal_onboarding.ui.pages import render_customer_overview_page, render_accounts_page, render_onboarding_page, render_features_page, render_support_page


def route_customer_portal_status() -> dict:
    return {
        "ok": True,
        "service": "zai-customer-portal-and-onboarding",
        "systems": [
            "customer_portal_dashboard",
            "customer_account_directory",
            "onboarding_wizard",
            "workspace_setup_plan",
            "plan_feature_access",
            "billing_handoff_draft",
            "support_ticket_flow",
            "welcome_checklist",
            "customer_export_tools",
            "customer_audit_log",
        ],
    }


def route_customer_overview() -> dict:
    return customer_overview()


def route_customer_accounts() -> dict:
    return {"customers": customer_directory(), "validation": customer_validation_report(), "create_plan": create_customer_plan("Demo", "demo@example.local")}


def route_customer_features(plan: str = "free") -> dict:
    return {"features": feature_catalog(), "validation": feature_validation_report(), "matrix": customer_feature_matrix(plan), "connector_access": feature_access(plan, "connectors")}


def route_customer_onboarding() -> dict:
    plan = build_onboarding_plan("cust_demo", "ws_demo")
    return {"steps": onboarding_steps(), "validation": onboarding_step_validation_report(), "plan": plan.to_dict(), "progress": onboarding_progress(plan.to_dict())}


def route_customer_onboarding_demo() -> dict:
    return onboarding_demo(".")


def route_customer_workspace_setup() -> dict:
    plan = workspace_setup_plan("org_demo", "ws_demo")
    return {"plan": plan, "gate": workspace_setup_gate(plan)}


def route_customer_billing_handoff() -> dict:
    customer = {"id": "cust_demo", "org_id": "org_demo", "plan": "free"}
    return {"handoff": billing_handoff_draft(customer), "upgrade": upgrade_request_plan(customer, "pro")}


def route_customer_support_demo() -> dict:
    return support_demo()


def route_customer_support_policy() -> dict:
    return support_policy()


def route_customer_export() -> dict:
    return {"bundle": customer_export_bundle(), "path": write_customer_export(".")}


def route_customer_action_demo() -> dict:
    return customer_action_demo(".")


def route_customer_audit() -> dict:
    return {"events": CustomerAuditLog().list_events()}


def route_customer_page() -> dict:
    return {"content_type": "text/html", "html": render_customer_overview_page()}


def route_customer_accounts_page() -> dict:
    return {"content_type": "text/html", "html": render_accounts_page()}


def route_customer_onboarding_page() -> dict:
    return {"content_type": "text/html", "html": render_onboarding_page()}


def route_customer_features_page() -> dict:
    return {"content_type": "text/html", "html": render_features_page()}


def route_customer_support_page() -> dict:
    return {"content_type": "text/html", "html": render_support_page()}
