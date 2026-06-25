from pathlib import Path
import tempfile

from zai_coder.payment_provider_sandbox.models import PaymentProviderConfig, CheckoutSessionDraft, SubscriptionRecord
from zai_coder.payment_provider_sandbox.env_validation import validate_payment_env
from zai_coder.payment_provider_sandbox.checkout import create_checkout_session_draft, checkout_session_payload
from zai_coder.payment_provider_sandbox.subscription import create_subscription, transition_subscription, subscription_lifecycle_manifest
from zai_coder.payment_provider_sandbox.webhooks import sign_sandbox_webhook, verify_sandbox_webhook, create_webhook_event_draft, webhook_event_policy
from zai_coder.payment_provider_sandbox.audit import PaymentAuditLog
from zai_coder.payment_provider_sandbox.plan_change import plan_change_workflow, failed_payment_policy
from zai_coder.payment_provider_sandbox.email_templates import billing_email_template, billing_email_manifest
from zai_coder.payment_provider_sandbox.safety import no_real_charge_gate, payment_apply_policy
from zai_coder.payment_provider_sandbox.ui.pages import render_payment_overview, render_checkout_page, render_subscription_page, render_webhooks_page
from zai_coder.payment_provider_sandbox.routes import (
    route_payment_status,
    route_payment_env_check,
    route_checkout_draft,
    route_subscription_lifecycle,
    route_webhook_draft,
    route_webhook_policy,
    route_plan_change,
    route_failed_payment_policy,
    route_billing_email_templates,
    route_no_real_charge_gate,
    route_payment_apply_policy,
    route_payment_audit,
    route_payment_page,
    route_payment_checkout_page,
    route_payment_subscription_page,
    route_payment_webhooks_page,
)


def test_config_and_env_validation():
    assert PaymentProviderConfig().validate() == []
    assert PaymentProviderConfig(mode="live").validate()
    assert validate_payment_env("sandbox", {})["ok"] is True
    assert validate_payment_env("stripe_sandbox", {})["ok"] is False
    assert validate_payment_env("sandbox", {"STRIPE_SECRET_KEY": "live"} )["ok"] is False


def test_checkout_draft():
    draft = create_checkout_session_draft("org1", "free")
    assert draft.validate() == []
    assert draft.amount_cents == 0
    payload = checkout_session_payload(draft)
    assert payload["no_real_charge"] is True
    bad = CheckoutSessionDraft("x", "org", "free", 1, success_url="https://example.com")
    assert bad.validate()


def test_subscription_lifecycle():
    sub = create_subscription("org1", "free", "trialing")
    active = transition_subscription(sub, "active")
    assert active.status == "active"
    assert "trialing" in subscription_lifecycle_manifest()
    try:
        transition_subscription(active, "trialing")
        assert False
    except ValueError:
        assert True
    assert SubscriptionRecord("", "", "", "bad").validate()


def test_webhook_scaffold():
    payload = {"hello": "world"}
    sig = sign_sandbox_webhook(payload)
    assert verify_sandbox_webhook(payload, sig)["ok"] is True
    assert verify_sandbox_webhook(payload, "bad")["ok"] is False
    event = create_webhook_event_draft("org1")
    assert event.signature
    assert webhook_event_policy()["real_webhooks_disabled"] is True


def test_audit_plan_change_email_safety():
    with tempfile.TemporaryDirectory() as td:
        audit = PaymentAuditLog(Path(td) / "audit.db")
        event = audit.record("org1", "actor", "checkout.draft_created", "target")
        assert audit.list_events("org1")[0]["id"] == event.id
    workflow = plan_change_workflow("org1", "free", "pro")
    assert workflow["dry_run"] is True
    assert workflow["direction"] == "upgrade"
    assert failed_payment_policy("pro")["safe_mode"] is True
    assert billing_email_template("payment_failed")["safe_mode"] is True
    assert "checkout_created" in billing_email_manifest()
    assert no_real_charge_gate()["allowed"] is True
    assert no_real_charge_gate(payload={"mode": "live"})["allowed"] is False
    assert payment_apply_policy()["real_charges_allowed"] is False


def test_ui_pages():
    assert "Payment Provider Sandbox" in render_payment_overview()
    assert "Checkout Draft" in render_checkout_page()
    assert "Subscription Workflow" in render_subscription_page()
    assert "Webhook Scaffold" in render_webhooks_page()


def test_routes(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert route_payment_status()["ok"] is True
    assert route_payment_env_check("sandbox")["ok"] is True
    assert route_checkout_draft("org_local", "free")["no_real_charge"] is True
    assert route_subscription_lifecycle()["demo"]["status"] == "active"
    assert route_webhook_draft("org_local")["verification"]["ok"] is True
    assert route_webhook_policy()["real_webhooks_disabled"] is True
    assert route_plan_change("free", "pro")["direction"] == "upgrade"
    assert route_failed_payment_policy("pro")["safe_mode"] is True
    assert route_billing_email_templates()["templates"]
    assert route_no_real_charge_gate()["allowed"] is True
    assert route_payment_apply_policy()["sandbox_only"] is True
    assert "events" in route_payment_audit()
    assert route_payment_page()["content_type"] == "text/html"
    assert route_payment_checkout_page()["content_type"] == "text/html"
    assert route_payment_subscription_page()["content_type"] == "text/html"
    assert route_payment_webhooks_page()["content_type"] == "text/html"


def test_docs_scripts_assets_exist():
    root = Path(__file__).resolve().parents[1]
    for rel in [
        "scripts/payments/payment-status.sh",
        "scripts/payments/payment-env-check.sh",
        "scripts/payments/checkout-draft.sh",
        "scripts/payments/subscription-lifecycle.sh",
        "scripts/payments/webhook-draft.sh",
        "scripts/payments/plan-change-workflow.sh",
        "scripts/payments/failed-payment-policy.sh",
        "scripts/payments/billing-email-templates.sh",
        "scripts/payments/no-real-charge-gate.sh",
        "scripts/payments/payment-audit.sh",
        "scripts/payments/payment-dashboard-export.sh",
        "docs/payments/PAYMENT_PROVIDER_SANDBOX_GUIDE.md",
        "docs/payments/NO_REAL_CHARGE_POLICY.md",
        "docs/payments/CHECKOUT_AND_SUBSCRIPTIONS.md",
        "docs/payments/WEBHOOK_VERIFIER_SCAFFOLD.md",
        "docs/payments/FAILED_PAYMENT_POLICY.md",
        "docs/payments/PAYMENT_AUDIT_LOG.md",
        "docs/requirements/NEXT_V23_PAYMENT_PROVIDER_SANDBOX_REQUIREMENTS.md",
        "assets/payments/payment_provider_sandbox_features.json",
    ]:
        assert (root / rel).exists(), rel
