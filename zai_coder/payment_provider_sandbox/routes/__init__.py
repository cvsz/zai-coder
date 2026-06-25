"""Payment Provider Sandbox route registry."""

from __future__ import annotations

import os

from zai_coder.payment_provider_sandbox.models import PaymentProviderConfig
from zai_coder.payment_provider_sandbox.env_validation import validate_payment_env
from zai_coder.payment_provider_sandbox.checkout import create_checkout_session_draft, checkout_session_payload
from zai_coder.payment_provider_sandbox.subscription import create_subscription, transition_subscription, subscription_lifecycle_manifest
from zai_coder.payment_provider_sandbox.webhooks import create_webhook_event_draft, verify_sandbox_webhook, webhook_event_policy
from zai_coder.payment_provider_sandbox.audit import PaymentAuditLog
from zai_coder.payment_provider_sandbox.plan_change import plan_change_workflow, failed_payment_policy
from zai_coder.payment_provider_sandbox.email_templates import billing_email_template, billing_email_manifest
from zai_coder.payment_provider_sandbox.safety import no_real_charge_gate, payment_apply_policy
from zai_coder.payment_provider_sandbox.ui.pages import render_payment_overview, render_checkout_page, render_subscription_page, render_webhooks_page


def route_payment_status() -> dict:
    return {
        "ok": True,
        "service": "zai-payment-provider-sandbox",
        "systems": [
            "sandbox_payment_provider_adapter",
            "checkout_session_draft",
            "subscription_lifecycle_model",
            "webhook_verifier_scaffold",
            "payment_audit_log",
            "plan_upgrade_downgrade_workflow",
            "failed_payment_policy",
            "billing_email_templates",
            "no_real_charge_safety_mode",
            "payment_provider_env_validation",
        ],
    }


def route_payment_env_check(provider: str = "sandbox") -> dict:
    return validate_payment_env(provider, dict(os.environ))


def route_checkout_draft(org_id: str = "org_local", plan_id: str = "free") -> dict:
    draft = create_checkout_session_draft(org_id, plan_id)
    PaymentAuditLog().record(org_id, "system", "checkout.draft_created", draft.id, "sandbox", draft.to_dict())
    return checkout_session_payload(draft)


def route_subscription_lifecycle() -> dict:
    sub = create_subscription("org_local", "free", "trialing")
    active = transition_subscription(sub, "active")
    return {"manifest": subscription_lifecycle_manifest(), "demo": active.to_dict()}


def route_webhook_draft(org_id: str = "org_local") -> dict:
    event = create_webhook_event_draft(org_id)
    return {"event": event.to_dict(), "verification": verify_sandbox_webhook(event.payload, event.signature)}


def route_webhook_policy() -> dict:
    return webhook_event_policy()


def route_plan_change(current_plan_id: str = "free", target_plan_id: str = "pro") -> dict:
    return plan_change_workflow("org_local", current_plan_id, target_plan_id)


def route_failed_payment_policy(plan_id: str = "pro") -> dict:
    return failed_payment_policy(plan_id)


def route_billing_email_templates() -> dict:
    return {"templates": [billing_email_template(kind) for kind in billing_email_manifest()]}


def route_no_real_charge_gate() -> dict:
    return no_real_charge_gate(PaymentProviderConfig(), {"mode": "sandbox", "live_charge": False})


def route_payment_apply_policy() -> dict:
    return payment_apply_policy()


def route_payment_audit() -> dict:
    return {"events": PaymentAuditLog().list_events("org_local")}


def route_payment_page() -> dict:
    return {"content_type": "text/html", "html": render_payment_overview()}


def route_payment_checkout_page() -> dict:
    return {"content_type": "text/html", "html": render_checkout_page()}


def route_payment_subscription_page() -> dict:
    return {"content_type": "text/html", "html": render_subscription_page()}


def route_payment_webhooks_page() -> dict:
    return {"content_type": "text/html", "html": render_webhooks_page()}
