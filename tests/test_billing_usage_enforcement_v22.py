from pathlib import Path
import tempfile

from zai_coder.billing_usage_enforcement.models import BillingAccount, BillingPlan, UsageEvent, WorkspaceUsageSummary
from zai_coder.billing_usage_enforcement.plans import plan_manifest, get_plan, plan_policy
from zai_coder.billing_usage_enforcement.ledger import UsageLedger
from zai_coder.billing_usage_enforcement.aggregation import aggregate_workspace_usage, aggregate_org_usage
from zai_coder.billing_usage_enforcement.enforcement import enforce_plan_limits, action_enforcement_decision
from zai_coder.billing_usage_enforcement.overage import calculate_overage_cents, overage_alerts
from zai_coder.billing_usage_enforcement.invoice import generate_invoice_draft, write_invoice_draft
from zai_coder.billing_usage_enforcement.audit import billing_audit_summary
from zai_coder.billing_usage_enforcement.ui.pages import render_billing_overview, render_plans_page, render_usage_page, render_invoice_page
from zai_coder.billing_usage_enforcement.routes import (
    route_billing_status,
    route_plan_manifest,
    route_plan_policy,
    route_record_usage_demo,
    route_usage_summary,
    route_org_usage_summary,
    route_enforcement,
    route_action_enforcement,
    route_overage_alerts,
    route_invoice_draft,
    route_invoice_write,
    route_billing_audit,
    route_billing_page,
    route_billing_plans_page,
    route_billing_usage_page,
    route_billing_invoice_page,
)


def test_models_validation():
    assert BillingAccount("ba1", "org1", "free", "active", "billing@example.com").validate() == []
    assert BillingAccount("", "", "", "bad", "no").validate()
    assert BillingPlan("p", "Plan", 0, 1, 1, 1, 1).validate() == []
    assert BillingPlan("", "", -1, -1, -1, -1, -1).validate()
    assert UsageEvent("u1", "org1", "ws1", "run").validate() == []


def test_plans():
    plans = plan_manifest()
    assert len(plans) >= 4
    assert get_plan("free").monthly_runs_limit > 0
    assert plan_policy("enterprise")["requires_contract"] is True


def test_ledger_aggregation_audit():
    with tempfile.TemporaryDirectory() as td:
        ledger = UsageLedger(Path(td) / "usage.db")
        ledger.record_usage("org1", "ws1", "run", 3)
        ledger.record_usage("org1", "ws1", "storage_mb", 50)
        ledger.record_usage("org1", "ws2", "run", 1)
        events = ledger.list_usage("org1")
        summary = aggregate_workspace_usage(events, "org1", "ws1")
        assert summary.monthly_runs == 3
        assert summary.storage_mb == 50
        org = aggregate_org_usage(events, "org1")
        assert "ws1" in org["workspaces"]
        ledger.record_audit("org1", "tester", "usage.recorded", "ws1")
        audit = billing_audit_summary("org1", ledger)
        assert audit["total"] == 1


def test_enforcement_overage_invoice(tmp_path):
    usage = WorkspaceUsageSummary("org1", "ws1", monthly_runs=251, storage_mb=600, provider_apply=11, seats=1, api_calls=0)
    decision = enforce_plan_limits("free", usage)
    assert decision["allowed"] is False
    assert "monthly_runs" in decision["blocked"]
    action = action_enforcement_decision("free", usage, "run")
    assert action["allowed"] is False
    over = calculate_overage_cents("free", usage)
    assert over["total_cents"] > 0
    alerts = overage_alerts("free", usage)
    assert alerts
    account = BillingAccount("ba1", "org1", "free", "active", "billing@example.com")
    invoice = generate_invoice_draft(account, usage)
    assert invoice.total_cents >= invoice.subtotal_cents
    path = write_invoice_draft(invoice, tmp_path)
    assert Path(path).exists()


def test_ui_pages():
    assert "Billing Usage Enforcement" in render_billing_overview()
    assert "Plans" in render_plans_page()
    assert "Usage" in render_usage_page()
    assert "Invoice Draft" in render_invoice_page()


def test_routes(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert route_billing_status()["ok"] is True
    assert route_plan_manifest()["plans"]
    assert route_plan_policy("free")["self_serve"] is True
    event = route_record_usage_demo()
    assert event["event_type"] == "run"
    assert route_usage_summary()["summary"]["monthly_runs"] >= 1
    assert "workspaces" in route_org_usage_summary()
    assert route_enforcement("free")["allowed"] is True
    assert route_action_enforcement("free", "run")["allowed"] is True
    assert "alerts" in route_overage_alerts("free")
    assert route_invoice_draft("free")["plan_id"] == "free"
    assert Path(route_invoice_write("free")["path"]).exists()
    assert "events" in route_billing_audit()
    assert route_billing_page()["content_type"] == "text/html"
    assert route_billing_plans_page()["content_type"] == "text/html"
    assert route_billing_usage_page()["content_type"] == "text/html"
    assert route_billing_invoice_page()["content_type"] == "text/html"


def test_docs_scripts_assets_exist():
    root = Path(__file__).resolve().parents[1]
    for rel in [
        "scripts/billing/billing-status.sh",
        "scripts/billing/billing-plans.sh",
        "scripts/billing/plan-policy.sh",
        "scripts/billing/usage-record-demo.sh",
        "scripts/billing/usage-summary.sh",
        "scripts/billing/quota-enforcement.sh",
        "scripts/billing/overage-alerts.sh",
        "scripts/billing/invoice-draft.sh",
        "scripts/billing/invoice-write.sh",
        "scripts/billing/billing-audit.sh",
        "scripts/billing/billing-dashboard-export.sh",
        "docs/billing/BILLING_USAGE_ENFORCEMENT_GUIDE.md",
        "docs/billing/BILLING_PLANS.md",
        "docs/billing/USAGE_LEDGER.md",
        "docs/billing/QUOTA_ENFORCEMENT.md",
        "docs/billing/INVOICE_DRAFTS.md",
        "docs/billing/BILLING_AUDIT_TRAIL.md",
        "docs/requirements/NEXT_V22_BILLING_USAGE_ENFORCEMENT_REQUIREMENTS.md",
        "assets/billing/billing_usage_enforcement_features.json",
    ]:
        assert (root / rel).exists(), rel
