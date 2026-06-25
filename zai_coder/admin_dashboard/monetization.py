"""Static monetization admin dashboard renderer."""

from __future__ import annotations

from html import escape
from typing import Iterable


def render_monetization_dashboard(plans: Iterable[dict], usage_summary: dict) -> str:
    rows = "\n".join(
        f"<tr><td>{escape(str(p['slug']))}</td><td>{escape(str(p['name']))}</td><td>{p['monthly_price_cents']}</td><td>{p['max_members']}</td></tr>"
        for p in plans
    )
    usage_rows = "\n".join(
        f"<tr><td>{escape(str(k))}</td><td>{escape(str(v))}</td></tr>"
        for k, v in sorted(usage_summary.items())
    )
    return f"""<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>ZAI Monetization Admin</title>
  <style>
    body {{ font-family: system-ui, sans-serif; margin: 2rem; background: #020617; color: #e2e8f0; }}
    table {{ border-collapse: collapse; width: 100%; margin: 1rem 0; }}
    th, td {{ border: 1px solid #334155; padding: 0.6rem; }}
    th {{ background: #1e293b; }}
    .card {{ border: 1px solid #334155; border-radius: 12px; padding: 1rem; margin-bottom: 1rem; }}
  </style>
</head>
<body>
  <h1>ZAI Monetization Admin</h1>
  <section class="card">
    <h2>Plans</h2>
    <table><thead><tr><th>Slug</th><th>Name</th><th>Monthly cents</th><th>Members</th></tr></thead><tbody>{rows}</tbody></table>
  </section>
  <section class="card">
    <h2>Usage Summary</h2>
    <table><thead><tr><th>Metric</th><th>Value</th></tr></thead><tbody>{usage_rows}</tbody></table>
  </section>
</body>
</html>
"""
