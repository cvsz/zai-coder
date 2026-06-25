"""Usage Analytics and Insights UI pages."""

from __future__ import annotations

from html import escape

from zai_coder.usage_analytics_insights.control import usage_analytics_status, analytics_overview
from zai_coder.usage_analytics_insights.privacy import analytics_retention_policy


def render_analytics_shell(title: str, body: str) -> str:
    return f"""<!doctype html><html><head><meta charset="utf-8"><title>{escape(title)}</title>
<style>
body{{font-family:system-ui;background:#020617;color:#e2e8f0;margin:0}}
nav{{background:#0f172a;padding:16px;display:flex;gap:14px;flex-wrap:wrap}}
a{{color:#7dd3fc;text-decoration:none}}
main{{padding:24px}}
.card{{border:1px solid #334155;border-radius:12px;padding:14px;margin:12px 0;background:#0f172a}}
pre{{background:#0f172a;border:1px solid #334155;border-radius:12px;padding:12px;white-space:pre-wrap}}
</style></head><body>
<nav><a href="/analytics">Overview</a><a href="/analytics/metrics">Metrics</a><a href="/analytics/insights">Insights</a><a href="/analytics/funnel">Funnel</a><a href="/analytics/privacy">Privacy</a></nav>
<main>{body}</main></body></html>"""


def render_analytics_overview_page() -> str:
    return render_analytics_shell("Usage Analytics", f"<h1>Usage Analytics and Insights</h1><pre>{escape(str(usage_analytics_status()))}</pre>")


def render_metrics_page() -> str:
    overview = analytics_overview()
    return render_analytics_shell("Usage Metrics", f"<h1>Metrics</h1><pre>{escape(str(overview['aggregate']))}</pre>")


def render_insights_page() -> str:
    overview = analytics_overview()
    return render_analytics_shell("Usage Insights", f"<h1>Insights</h1><pre>{escape(str(overview['insights']))}</pre>")


def render_funnel_page() -> str:
    overview = analytics_overview()
    return render_analytics_shell("Adoption Funnel", f"<h1>Funnel</h1><pre>{escape(str(overview['funnel']))}</pre>")


def render_privacy_page() -> str:
    return render_analytics_shell("Analytics Privacy", f"<h1>Privacy</h1><pre>{escape(str(analytics_retention_policy()))}</pre>")
