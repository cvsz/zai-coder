"""Notification and Communication Center UI pages."""

from __future__ import annotations

from html import escape

from zai_coder.notification_communication_center.control import notification_center_status, notification_center_overview
from zai_coder.notification_communication_center.channels import channel_catalog
from zai_coder.notification_communication_center.templates import notification_template_registry
from zai_coder.notification_communication_center.preferences import preference_catalog


def render_notification_shell(title: str, body: str) -> str:
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
<nav><a href="/notifications">Overview</a><a href="/notifications/channels">Channels</a><a href="/notifications/templates">Templates</a><a href="/notifications/preferences">Preferences</a><a href="/notifications/drafts">Drafts</a></nav>
<main>{body}</main></body></html>"""


def render_notifications_overview_page() -> str:
    return render_notification_shell("Notification and Communication Center", f"<h1>Notification and Communication Center</h1><pre>{escape(str(notification_center_status()))}</pre>")


def render_channels_page() -> str:
    rows = "\n".join(f"<tr><td>{escape(c['id'])}</td><td>{escape(c['name'])}</td><td>{c['enabled']}</td><td>{c['external']}</td></tr>" for c in channel_catalog())
    return render_notification_shell("Notification Channels", f"<h1>Channels</h1><table><tbody>{rows}</tbody></table>")


def render_templates_page() -> str:
    rows = "\n".join(f"<tr><td>{escape(t['title'])}</td><td>{escape(t['channel'])}</td><td>{escape(t['status'])}</td></tr>" for t in notification_template_registry())
    return render_notification_shell("Notification Templates", f"<h1>Templates</h1><table><tbody>{rows}</tbody></table>")


def render_preferences_page() -> str:
    rows = "\n".join(f"<tr><td>{escape(p['customer_id'])}</td><td>{escape(p['channel'])}</td><td>{escape(p['topic'])}</td><td>{p['enabled']}</td></tr>" for p in preference_catalog())
    return render_notification_shell("Notification Preferences", f"<h1>Preferences</h1><table><tbody>{rows}</tbody></table>")


def render_drafts_page() -> str:
    overview = notification_center_overview()
    return render_notification_shell("Notification Drafts", f"<h1>Drafts</h1><pre>{escape(str(overview['demo']['draft']))}</pre>")
