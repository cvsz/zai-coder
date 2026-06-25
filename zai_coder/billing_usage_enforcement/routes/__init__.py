"""Billing usage enforcement route registry."""

from __future__ import annotations

from zai_coder.billing_usage_enforcement.models import BillingAccount, WorkspaceUsageSummary
from zai_coder.billing_usage_enforcement.plans import plan_manifest, plan_policy
from zai_coder.billing_usage_enforcement.ledger import UsageLedger
from zai_coder.billing_usage_enforcement.aggregation import aggregate_workspace_usage, aggregate_org_usage
from zai_coder.billing_usage_enforcement.enforcement import enforce_plan_limits, action_enforcement_decision
from zai_coder.billing_usage_enforcement.overage import overage_alerts, calculate_overage_cents
from zai_coder.billing_usage_enforcement.invoice import generate_invoice_draft, write_invoice_draft
from zai_coder.billing_usage_enforcement.audit import billing_audit_summary
from zai_coder.billing_usage_enforcement.ui.pages import render_billing_overview, render_plans_page, render_usage_page, render_invoice_page


def route_billing_status() -> dict:
    return {
        "ok": True,
        "service": "zai-billing-usage-enforcement",
        "systems": [
            "tenant_billing_account_model",
            "usage_event_ledger",
            "workspace_usage_aggregation",
            "billing_plans",
            "quota_to_plan_enforcement",
            "trial_free_pro_enterprise_plan_policy",
            "invoice_draft_generator",
            "overage_alert_policy",
            "usage_dashboard",
            "billing_audit_trail",
        ],
    }


def route_plan_manifest() -> dict:
    return {"plans": plan_manifest()}


def route_plan_policy(plan_id: str = "free") -> dict:
    return plan_policy(plan_id)


def route_record_usage_demo() -> dict:
    ledger = UsageLedger()
    event = ledger.record_usage("org_local", "ws_default", "run", 1, "count", "demo")
    ledger.record_audit("org_local", "demo", "usage.recorded", event.id, {"event_type": "run"})
    return event.to_dict()


def route_usage_summary() -> dict:
    ledger = UsageLedger()
    events = ledger.list_usage("org_local", "ws_default")
    summary = aggregate_workspace_usage(events, "org_local", "ws_default")
    return {"summary": summary.to_dict(), "events": events}


def route_org_usage_summary() -> dict:
    ledger = UsageLedger()
    events = ledger.list_usage("org_local")
    return aggregate_org_usage(events, "org_local")


def route_enforcement(plan_id: str = "free") -> dict:
    usage = WorkspaceUsageSummary("org_local", "ws_default", monthly_runs=10, storage_mb=20, provider_apply=1, seats=1, api_calls=100)
    return enforce_plan_limits(plan_id, usage)


def route_action_enforcement(plan_id: str = "free", action: str = "run") -> dict:
    usage = WorkspaceUsageSummary("org_local", "ws_default", monthly_runs=10, storage_mb=20, provider_apply=1, seats=1, api_calls=100)
    return action_enforcement_decision(plan_id, usage, action)


def route_overage_alerts(plan_id: str = "free") -> dict:
    usage = WorkspaceUsageSummary("org_local", "ws_default", monthly_runs=225, storage_mb=500, provider_apply=9, seats=1, api_calls=100)
    return {"alerts": overage_alerts(plan_id, usage), "overage": calculate_overage_cents(plan_id, usage)}


def route_invoice_draft(plan_id: str = "free") -> dict:
    account = BillingAccount("ba_local", "org_local", plan_id, "active", "billing@example.com")
    usage = WorkspaceUsageSummary("org_local", "ws_default", 10, 20, 1, 1, 100)
    invoice = generate_invoice_draft(account, usage)
    return invoice.to_dict()


def route_invoice_write(plan_id: str = "free") -> dict:
    account = BillingAccount("ba_local", "org_local", plan_id, "active", "billing@example.com")
    usage = WorkspaceUsageSummary("org_local", "ws_default", 10, 20, 1, 1, 100)
    invoice = generate_invoice_draft(account, usage)
    return {"path": write_invoice_draft(invoice)}


def route_billing_audit() -> dict:
    return billing_audit_summary("org_local")


def route_billing_page() -> dict:
    return {"content_type": "text/html", "html": render_billing_overview()}


def route_billing_plans_page() -> dict:
    return {"content_type": "text/html", "html": render_plans_page()}


def route_billing_usage_page() -> dict:
    return {"content_type": "text/html", "html": render_usage_page()}


def route_billing_invoice_page() -> dict:
    return {"content_type": "text/html", "html": render_invoice_page()}
