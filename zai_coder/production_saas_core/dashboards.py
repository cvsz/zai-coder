"""Production SaaS dashboard renderers."""

from __future__ import annotations

from html import escape
from typing import Iterable


def _table(rows: Iterable[dict], fields: list[str]) -> str:
    header = "".join(f"<th>{escape(field)}</th>" for field in fields)
    body = "\n".join(
        "<tr>" + "".join(f"<td>{escape(str(row.get(field, '')))}</td>" for field in fields) + "</tr>"
        for row in rows
    )
    return f"<table><thead><tr>{header}</tr></thead><tbody>{body}</tbody></table>"


def render_billing_dashboard(plans: list[dict], subscriptions: list[dict]) -> str:
    return f"""<!doctype html><html><head><meta charset='utf-8'><title>Billing</title></head><body>
<h1>Billing Dashboard</h1>
<h2>Plans</h2>{_table(plans, ['slug', 'name', 'monthly_price_cents', 'max_members'])}
<h2>Subscriptions</h2>{_table(subscriptions, ['id', 'account_id', 'plan_slug', 'status'])}
</body></html>
"""


def render_usage_dashboard(usage_rows: list[dict], quota_rows: list[dict]) -> str:
    return f"""<!doctype html><html><head><meta charset='utf-8'><title>Usage</title></head><body>
<h1>Usage Dashboard</h1>
<h2>Usage</h2>{_table(usage_rows, ['resource', 'units', 'source'])}
<h2>Quota</h2>{_table(quota_rows, ['resource', 'used', 'limit', 'allowed'])}
</body></html>
"""


def render_audit_dashboard(events: list[dict]) -> str:
    return f"""<!doctype html><html><head><meta charset='utf-8'><title>Audit</title></head><body>
<h1>Audit Dashboard</h1>
{_table(events, ['actor', 'action', 'target', 'created_at'])}
</body></html>
"""


def render_settings_dashboard(settings: dict) -> str:
    rows = [{"key": key, "value": value} for key, value in sorted(settings.items())]
    return f"""<!doctype html><html><head><meta charset='utf-8'><title>Settings</title></head><body>
<h1>Admin Settings</h1>
{_table(rows, ['key', 'value'])}
</body></html>
"""
