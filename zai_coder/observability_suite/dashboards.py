"""Execution/provider dashboard renderers."""

from __future__ import annotations

from html import escape


def render_observability_shell(title: str, body: str) -> str:
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
<nav><a href="/observability">Overview</a><a href="/observability/metrics">Metrics</a><a href="/observability/alerts">Alerts</a><a href="/observability/health">Health</a><a href="/observability/incidents">Incidents</a></nav>
<main>{body}</main></body></html>"""


def render_observability_overview() -> str:
    body = """
<h1>Observability Suite</h1>
<div class="card"><h2>Metrics</h2><p>Prometheus-style metrics endpoint.</p></div>
<div class="card"><h2>Events</h2><p>Structured event bus for execution and provider actions.</p></div>
<div class="card"><h2>Alerts</h2><p>Alert rules for health, queues, and provider failures.</p></div>
<div class="card"><h2>Incidents</h2><p>Incident report generator and recovery timeline.</p></div>
"""
    return render_observability_shell("Observability", body)


def render_metrics_dashboard(samples: list[dict]) -> str:
    rows = "\n".join(
        f"<tr><td>{escape(s.get('name',''))}</td><td>{escape(str(s.get('value','')))}</td><td>{escape(s.get('kind',''))}</td><td>{escape(str(s.get('labels',{})))}</td></tr>"
        for s in samples
    )
    return render_observability_shell("Metrics", f"<h1>Metrics</h1><table><tbody>{rows}</tbody></table>")


def render_alerts_dashboard(alerts: list[dict]) -> str:
    rows = "\n".join(
        f"<tr><td>{escape(a['rule']['name'])}</td><td>{escape(a['rule']['severity'])}</td><td>{escape(str(a['sample']['value']))}</td></tr>"
        for a in alerts
    )
    return render_observability_shell("Alerts", f"<h1>Alerts</h1><table><tbody>{rows}</tbody></table>")


def render_health_trends_dashboard(snapshots: list[dict]) -> str:
    rows = "\n".join(
        f"<tr><td>{escape(s['ts'])}</td><td>{escape(s['status'])}</td><td>{s['ok_ratio']}</td><td>{s['latency_ms']}</td></tr>"
        for s in snapshots
    )
    return render_observability_shell("Health Trends", f"<h1>Health Trends</h1><table><tbody>{rows}</tbody></table>")
