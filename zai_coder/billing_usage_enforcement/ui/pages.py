"""Billing dashboard pages."""

from __future__ import annotations

from html import escape

from zai_coder.billing_usage_enforcement.plans import plan_manifest
from zai_coder.billing_usage_enforcement.models import WorkspaceUsageSummary, BillingAccount
from zai_coder.billing_usage_enforcement.invoice import generate_invoice_draft
from zai_coder.billing_usage_enforcement.overage import overage_alerts


def render_billing_shell(title: str, body: str) -> str:
    return f"""<!doctype html><html><head><meta charset="utf-8"><title>{escape(title)}</title>
<style>
body{{font-family:system-ui;background:#020617;color:#e2e8f0;margin:0}}
nav{{background:#0f172a;padding:16px;display:flex;gap:14px}}
a{{color:#7dd3fc;text-decoration:none}}
main{{padding:24px}}
.card{{border:1px solid #334155;border-radius:12px;padding:14px;margin:12px 0;background:#0f172a}}
table{{width:100%;border-collapse:collapse}}td,th{{border:1px solid #334155;padding:8px}}
pre{{background:#0f172a;border:1px solid #334155;border-radius:12px;padding:12px;white-space:pre-wrap}}
</style></head><body>
<nav><a href="/billing">Overview</a><a href="/billing/plans">Plans</a><a href="/billing/usage">Usage</a><a href="/billing/invoice">Invoice</a></nav>
<main>{body}</main></body></html>"""


def render_billing_overview() -> str:
    body = """
<h1>Billing Usage Enforcement</h1>
<div class="card"><h2>Plans</h2><p>Trial, Free, Pro, and Enterprise policy.</p></div>
<div class="card"><h2>Usage</h2><p>Workspace usage ledger and aggregation.</p></div>
<div class="card"><h2>Enforcement</h2><p>Quota-to-plan enforcement and overage alerts.</p></div>
<div class="card"><h2>Audit</h2><p>Billing audit trail and invoice drafts.</p></div>
"""
    return render_billing_shell("Billing", body)


def render_plans_page() -> str:
    rows = "\n".join(f"<tr><td>{escape(p['id'])}</td><td>{escape(p['name'])}</td><td>{p['monthly_price_cents']}</td><td>{p['monthly_runs_limit']}</td></tr>" for p in plan_manifest())
    return render_billing_shell("Plans", f"<h1>Plans</h1><table><tbody>{rows}</tbody></table>")


def render_usage_page() -> str:
    usage = WorkspaceUsageSummary("org_local", "ws_default", monthly_runs=10, storage_mb=20, provider_apply=1, seats=1, api_calls=100)
    alerts = overage_alerts("free", usage)
    return render_billing_shell("Usage", f"<h1>Usage</h1><pre>{escape(str({'usage': usage.to_dict(), 'alerts': alerts}))}</pre>")


def render_invoice_page() -> str:
    account = BillingAccount("ba_local", "org_local", "free", "active", "billing@example.com")
    usage = WorkspaceUsageSummary("org_local", "ws_default", 10, 20, 1, 1, 100)
    invoice = generate_invoice_draft(account, usage)
    return render_billing_shell("Invoice Draft", f"<h1>Invoice Draft</h1><pre>{escape(str(invoice.to_dict()))}</pre>")
