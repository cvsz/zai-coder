"""Customer Portal and Onboarding UI pages."""

from __future__ import annotations

from html import escape

from zai_coder.customer_portal_onboarding.control import customer_portal_status, customer_overview
from zai_coder.customer_portal_onboarding.accounts import customer_directory
from zai_coder.customer_portal_onboarding.features import feature_catalog
from zai_coder.customer_portal_onboarding.onboarding import onboarding_steps


def render_customer_shell(title: str, body: str) -> str:
    return f"""<!doctype html><html><head><meta charset="utf-8"><title>{escape(title)}</title>
<style>
body{{font-family:system-ui;background:#020617;color:#e2e8f0;margin:0}}
nav{{background:#0f172a;padding:16px;display:flex;gap:14px;flex-wrap:wrap}}
a{{color:#7dd3fc;text-decoration:none}}
main{{padding:24px}}
.card{{border:1px solid #334155;border-radius:12px;padding:14px;margin:12px 0;background:#0f172a}}
table{{width:100%;border-collapse:collapse}}td,th{{border:1px solid #334155;padding:8px}}
pre{{background:#0f172a;border:1px solid #334155;border-radius:12px;padding:12px;white-space:pre-wrap}}
</style></head><body>
<nav><a href="/customer">Overview</a><a href="/customer/accounts">Accounts</a><a href="/customer/onboarding">Onboarding</a><a href="/customer/features">Features</a><a href="/customer/support">Support</a></nav>
<main>{body}</main></body></html>"""


def render_customer_overview_page() -> str:
    return render_customer_shell("Customer Portal", f"<h1>Customer Portal and Onboarding</h1><pre>{escape(str(customer_portal_status()))}</pre>")


def render_accounts_page() -> str:
    rows = "\n".join(f"<tr><td>{escape(c['id'])}</td><td>{escape(c['name'])}</td><td>{escape(c['plan'])}</td><td>{escape(c['status'])}</td></tr>" for c in customer_directory())
    return render_customer_shell("Customer Accounts", f"<h1>Accounts</h1><table><tbody>{rows}</tbody></table>")


def render_onboarding_page() -> str:
    rows = "\n".join(f"<tr><td>{escape(s['id'])}</td><td>{escape(s['title'])}</td><td>{escape(s['owner'])}</td><td>{escape(s['status'])}</td></tr>" for s in onboarding_steps())
    return render_customer_shell("Onboarding", f"<h1>Onboarding</h1><table><tbody>{rows}</tbody></table>")


def render_features_page() -> str:
    rows = "\n".join(f"<tr><td>{escape(f['id'])}</td><td>{escape(f['name'])}</td><td>{escape(f['required_plan'])}</td><td>{f['enabled']}</td></tr>" for f in feature_catalog())
    return render_customer_shell("Customer Features", f"<h1>Features</h1><table><tbody>{rows}</tbody></table>")


def render_support_page() -> str:
    return render_customer_shell("Customer Support", "<h1>Support</h1><p>Local support ticket flow is enabled. External email sending is disabled.</p>")
