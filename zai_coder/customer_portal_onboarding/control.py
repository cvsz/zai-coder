"""Customer portal and onboarding control helpers."""

from __future__ import annotations

from .accounts import customer_directory, customer_validation_report, create_customer_plan, find_customer
from .features import feature_catalog, feature_validation_report, customer_feature_matrix
from .onboarding import build_onboarding_plan, onboarding_progress, write_onboarding_plan, onboarding_step_validation_report
from .workspace_setup import workspace_setup_plan, workspace_setup_gate
from .billing_handoff import billing_handoff_draft, upgrade_request_plan
from .support import SupportTicketStore, support_policy
from .exporter import write_customer_export, customer_export_bundle
from .audit import CustomerAuditLog


def customer_portal_status() -> dict:
    return {
        "ok": True,
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


def customer_overview() -> dict:
    return {
        "status": customer_portal_status(),
        "customers": customer_directory(),
        "customer_validation": customer_validation_report(),
        "features": feature_catalog(),
        "feature_validation": feature_validation_report(),
        "onboarding_validation": onboarding_step_validation_report(),
        "feature_matrix_free": customer_feature_matrix("free"),
    }


def onboarding_demo(root: str = ".") -> dict:
    customer = find_customer("cust_demo")
    plan = build_onboarding_plan(customer.id, "ws_demo")
    path = write_onboarding_plan(plan, root)
    progress = onboarding_progress(plan.to_dict())
    setup = workspace_setup_plan(customer.org_id, "ws_demo")
    billing = billing_handoff_draft(customer.to_dict())
    audit = CustomerAuditLog().record("system", "onboarding.plan_created", plan.id, {"customer_id": customer.id})
    return {"customer": customer.to_dict(), "plan": plan.to_dict(), "progress": progress, "path": path, "workspace_setup": setup, "billing": billing, "audit": audit.to_dict()}


def support_demo(db_path: str = "data/customer-portal.db") -> dict:
    store = SupportTicketStore(db_path)
    ticket = store.create_ticket("cust_demo", "Need help completing onboarding", "normal", "onboarding", "customer")
    audit = CustomerAuditLog(db_path).record("customer", "support.ticket_created", ticket.id, ticket.to_dict(), "cust_demo", "org_demo", "ws_demo")
    return {"ticket": ticket.to_dict(), "tickets": store.list_tickets("cust_demo"), "policy": support_policy(), "audit": audit.to_dict()}


def customer_action_demo(root: str = ".") -> dict:
    create_plan = create_customer_plan("Acme Demo", "owner@acme.example", "pro")
    export_path = write_customer_export(root)
    return {
        "create_customer": create_plan,
        "upgrade": upgrade_request_plan({"id": "cust_demo", "org_id": "org_demo", "plan": "free"}, "pro"),
        "workspace_gate": workspace_setup_gate(workspace_setup_plan(), "", False),
        "export_path": export_path,
        "export_bundle": customer_export_bundle(),
    }
