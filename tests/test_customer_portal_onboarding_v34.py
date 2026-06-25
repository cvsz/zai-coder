from pathlib import Path

from zai_coder.customer_portal_onboarding.models import CustomerAccount, PortalFeature, OnboardingStep, OnboardingPlan, SupportTicket
from zai_coder.customer_portal_onboarding.accounts import customer_directory, find_customer, customer_validation_report, create_customer_plan
from zai_coder.customer_portal_onboarding.features import feature_catalog, feature_validation_report, feature_access, customer_feature_matrix
from zai_coder.customer_portal_onboarding.onboarding import onboarding_steps, onboarding_step_validation_report, build_onboarding_plan, onboarding_progress, write_onboarding_plan
from zai_coder.customer_portal_onboarding.workspace_setup import workspace_setup_plan, workspace_setup_gate
from zai_coder.customer_portal_onboarding.billing_handoff import billing_handoff_draft, upgrade_request_plan
from zai_coder.customer_portal_onboarding.support import SupportTicketStore, support_policy
from zai_coder.customer_portal_onboarding.exporter import redacted_customer, customer_export_bundle, write_customer_export
from zai_coder.customer_portal_onboarding.audit import CustomerAuditLog
from zai_coder.customer_portal_onboarding.control import customer_portal_status, customer_overview, onboarding_demo, support_demo, customer_action_demo
from zai_coder.customer_portal_onboarding.ui.pages import render_customer_overview_page, render_accounts_page, render_onboarding_page, render_features_page, render_support_page
from zai_coder.customer_portal_onboarding.routes import (
    route_customer_portal_status,
    route_customer_overview,
    route_customer_accounts,
    route_customer_features,
    route_customer_onboarding,
    route_customer_onboarding_demo,
    route_customer_workspace_setup,
    route_customer_billing_handoff,
    route_customer_support_demo,
    route_customer_support_policy,
    route_customer_export,
    route_customer_action_demo,
    route_customer_audit,
    route_customer_page,
    route_customer_accounts_page,
    route_customer_onboarding_page,
    route_customer_features_page,
    route_customer_support_page,
)


def test_models_validation():
    assert CustomerAccount("c", "o", "Customer", "owner@example.local").validate() == []
    assert CustomerAccount("", "", "", "bad", plan="bad", status="bad").validate()
    assert PortalFeature("f", "Feature").validate() == []
    assert PortalFeature("../bad", "", required_plan="bad").validate()
    assert OnboardingStep("s", "Step", "Description").validate() == []
    assert OnboardingStep("", "", "", owner="bad", status="bad", order=-1).validate()
    assert SupportTicket("t", "c", "Help").validate() == []
    assert SupportTicket("", "", "", priority="bad", status="bad").validate()


def test_accounts_features_onboarding(tmp_path):
    assert customer_directory()
    assert find_customer("cust_demo").id == "cust_demo"
    assert customer_validation_report()["ok"] is True
    assert create_customer_plan("Acme", "owner@acme.example", "pro")["allowed"] is True
    assert feature_catalog()
    assert feature_validation_report()["ok"] is True
    assert feature_access("free", "dashboard")["allowed"] is True
    assert feature_access("free", "connectors")["allowed"] is False
    assert customer_feature_matrix("enterprise")["features"]
    assert onboarding_steps()
    assert onboarding_step_validation_report()["ok"] is True
    plan = build_onboarding_plan("cust_demo", "ws_demo")
    assert plan.dry_run is True
    progress = onboarding_progress(plan.to_dict())
    assert progress["percent_complete"] == 0
    path = write_onboarding_plan(plan, tmp_path)
    assert Path(path).exists()


def test_workspace_billing_support_export_audit(tmp_path):
    setup = workspace_setup_plan("org_demo", "ws_demo")
    assert setup["dry_run"] is True
    assert workspace_setup_gate(setup)["allowed"] is True
    assert workspace_setup_gate(setup, apply_requested=True)["allowed"] is False
    customer = find_customer("cust_demo").to_dict()
    handoff = billing_handoff_draft(customer)
    assert handoff["no_real_charge"] is True
    assert upgrade_request_plan(customer, "pro")["allowed"] is True
    store = SupportTicketStore(tmp_path / "customer.db")
    ticket = store.create_ticket("cust_demo", "Need help", "normal", "onboarding")
    assert store.list_tickets("cust_demo")[0]["id"] == ticket.id
    assert support_policy()["no_external_email_send"] is True
    redacted = redacted_customer(customer)
    assert "***@" in redacted["owner_email"]
    bundle = customer_export_bundle()
    assert bundle["external_publish"] is False
    export = write_customer_export(tmp_path)
    assert Path(export).exists()
    audit = CustomerAuditLog(tmp_path / "customer.db")
    event = audit.record("tester", "customer.test", "target")
    assert audit.list_events()[0]["id"] == event.id


def test_control_ui_routes(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert customer_portal_status()["ok"] is True
    assert customer_overview()["status"]["ok"] is True
    demo = onboarding_demo(str(tmp_path))
    assert Path(demo["path"]).exists()
    support = support_demo(str(tmp_path / "support.db"))
    assert support["ticket"]["id"].startswith("ticket_")
    action = customer_action_demo(str(tmp_path))
    assert Path(action["export_path"]).exists()
    assert "Customer Portal and Onboarding" in render_customer_overview_page()
    assert "Accounts" in render_accounts_page()
    assert "Onboarding" in render_onboarding_page()
    assert "Features" in render_features_page()
    assert "Support" in render_support_page()
    assert route_customer_portal_status()["ok"] is True
    assert route_customer_overview()["status"]["ok"] is True
    assert route_customer_accounts()["validation"]["ok"] is True
    assert route_customer_features("free")["connector_access"]["allowed"] is False
    assert route_customer_onboarding()["plan"]["dry_run"] is True
    assert Path(route_customer_onboarding_demo()["path"]).exists()
    assert route_customer_workspace_setup()["gate"]["allowed"] is True
    assert route_customer_billing_handoff()["handoff"]["no_real_charge"] is True
    assert route_customer_support_demo()["ticket"]["id"].startswith("ticket_")
    assert route_customer_support_policy()["local_ticket_flow"] is True
    assert Path(route_customer_export()["path"]).exists()
    assert Path(route_customer_action_demo()["export_path"]).exists()
    assert "events" in route_customer_audit()
    assert route_customer_page()["content_type"] == "text/html"
    assert route_customer_accounts_page()["content_type"] == "text/html"
    assert route_customer_onboarding_page()["content_type"] == "text/html"
    assert route_customer_features_page()["content_type"] == "text/html"
    assert route_customer_support_page()["content_type"] == "text/html"


def test_docs_scripts_assets_exist():
    root = Path(__file__).resolve().parents[1]
    for rel in [
        "scripts/customer-portal/customer-status.sh",
        "scripts/customer-portal/customer-accounts.sh",
        "scripts/customer-portal/customer-features.sh",
        "scripts/customer-portal/customer-onboarding.sh",
        "scripts/customer-portal/onboarding-demo.sh",
        "scripts/customer-portal/workspace-setup.sh",
        "scripts/customer-portal/billing-handoff.sh",
        "scripts/customer-portal/support-demo.sh",
        "scripts/customer-portal/customer-export.sh",
        "scripts/customer-portal/customer-action-demo.sh",
        "scripts/customer-portal/customer-audit.sh",
        "scripts/customer-portal/customer-dashboard-export.sh",
        "docs/customer-portal/CUSTOMER_PORTAL_ONBOARDING_GUIDE.md",
        "docs/customer-portal/ONBOARDING_WIZARD.md",
        "docs/customer-portal/FEATURE_ACCESS.md",
        "docs/customer-portal/BILLING_HANDOFF.md",
        "docs/customer-portal/SUPPORT_TICKETS.md",
        "docs/customer-portal/CUSTOMER_EXPORT_POLICY.md",
        "docs/requirements/NEXT_V34_CUSTOMER_PORTAL_ONBOARDING_REQUIREMENTS.md",
        "assets/customer-portal/customer_portal_onboarding_features.json",
    ]:
        assert (root / rel).exists(), rel
