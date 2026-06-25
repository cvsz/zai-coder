"""Feedback and Roadmap Center UI pages."""

from __future__ import annotations

from html import escape

from zai_coder.feedback_roadmap_center.control import feedback_roadmap_status, feedback_roadmap_overview
from zai_coder.feedback_roadmap_center.roadmap import roadmap_registry, roadmap_by_visibility


def render_roadmap_shell(title: str, body: str) -> str:
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
<nav><a href="/roadmap">Overview</a><a href="/roadmap/feedback">Feedback</a><a href="/roadmap/items">Roadmap</a><a href="/roadmap/customer-view">Customer View</a><a href="/roadmap/prioritization">Prioritization</a></nav>
<main>{body}</main></body></html>"""


def render_roadmap_overview_page() -> str:
    return render_roadmap_shell("Feedback and Roadmap Center", f"<h1>Feedback and Roadmap Center</h1><pre>{escape(str(feedback_roadmap_status()))}</pre>")


def render_feedback_page() -> str:
    overview = feedback_roadmap_overview()
    return render_roadmap_shell("Feedback Inbox", f"<h1>Feedback</h1><pre>{escape(str({'feedback_count': overview['feedback_count'], 'links': overview['links']}))}</pre>")


def render_roadmap_items_page() -> str:
    rows = "\n".join(f"<tr><td>{escape(i['id'])}</td><td>{escape(i['title'])}</td><td>{escape(i['horizon'])}</td><td>{escape(i['status'])}</td></tr>" for i in roadmap_registry())
    return render_roadmap_shell("Roadmap Items", f"<h1>Roadmap</h1><table><tbody>{rows}</tbody></table>")


def render_customer_view_page() -> str:
    rows = "\n".join(f"<tr><td>{escape(i['title'])}</td><td>{escape(i['horizon'])}</td><td>{escape(i['status'])}</td></tr>" for i in roadmap_by_visibility("customer"))
    return render_roadmap_shell("Customer Roadmap View", f"<h1>Customer View</h1><table><tbody>{rows}</tbody></table>")


def render_prioritization_page() -> str:
    overview = feedback_roadmap_overview()
    return render_roadmap_shell("Roadmap Prioritization", f"<h1>Prioritization</h1><pre>{escape(str(overview['prioritization']))}</pre>")
