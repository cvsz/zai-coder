"""Payment sandbox dashboard pages."""

from __future__ import annotations

from html import escape

from zai_coder.payment_provider_sandbox.checkout import create_checkout_session_draft, checkout_session_payload
from zai_coder.payment_provider_sandbox.plan_change import plan_change_workflow, failed_payment_policy
from zai_coder.payment_provider_sandbox.email_templates import billing_email_manifest


def render_payment_shell(title: str, body: str) -> str:
    return f"""<!doctype html><html><head><meta charset="utf-8"><title>{escape(title)}</title>
<style>
body{{font-family:system-ui;background:#020617;color:#e2e8f0;margin:0}}
nav{{background:#0f172a;padding:16px;display:flex;gap:14px}}
a{{color:#7dd3fc;text-decoration:none}}
main{{padding:24px}}
.card{{border:1px solid #334155;border-radius:12px;padding:14px;margin:12px 0;background:#0f172a}}
pre{{background:#0f172a;border:1px solid #334155;border-radius:12px;padding:12px;white-space:pre-wrap}}
</style></head><body>
<nav><a href="/payments">Overview</a><a href="/payments/checkout">Checkout</a><a href="/payments/subscription">Subscription</a><a href="/payments/webhooks">Webhooks</a></nav>
<main>{body}</main></body></html>"""


def render_payment_overview() -> str:
    body = """
<h1>Payment Provider Sandbox</h1>
<div class="card"><h2>No Real Charge</h2><p>Sandbox-only payment provider adapter.</p></div>
<div class="card"><h2>Checkout Draft</h2><p>Reviewable checkout session draft.</p></div>
<div class="card"><h2>Subscription Lifecycle</h2><p>Sandbox subscription transition model.</p></div>
<div class="card"><h2>Webhook Scaffold</h2><p>Verifier scaffold for sandbox events.</p></div>
"""
    return render_payment_shell("Payment Provider Sandbox", body)


def render_checkout_page() -> str:
    draft = create_checkout_session_draft("org_local", "free")
    payload = checkout_session_payload(draft)
    return render_payment_shell("Checkout Draft", f"<h1>Checkout Draft</h1><pre>{escape(str(payload))}</pre>")


def render_subscription_page() -> str:
    workflow = plan_change_workflow("org_local", "free", "pro")
    policy = failed_payment_policy("pro")
    return render_payment_shell("Subscription", f"<h1>Subscription Workflow</h1><pre>{escape(str({'workflow': workflow, 'failed_payment_policy': policy}))}</pre>")


def render_webhooks_page() -> str:
    return render_payment_shell("Webhooks", f"<h1>Webhook Scaffold</h1><pre>{escape(str({'templates': billing_email_manifest()}))}</pre>")
