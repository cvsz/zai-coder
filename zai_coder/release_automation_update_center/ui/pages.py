"""Release center dashboard pages."""

from __future__ import annotations

from html import escape

from zai_coder.release_automation_update_center.control import release_center_status, release_plan_demo, update_plan_demo, rollback_migration_demo
from zai_coder.release_automation_update_center.channels import release_channel_manifest


def render_release_shell(title: str, body: str) -> str:
    return f"""<!doctype html><html><head><meta charset="utf-8"><title>{escape(title)}</title>
<style>
body{{font-family:system-ui;background:#020617;color:#e2e8f0;margin:0}}
nav{{background:#0f172a;padding:16px;display:flex;gap:14px}}
a{{color:#7dd3fc;text-decoration:none}}
main{{padding:24px}}
.card{{border:1px solid #334155;border-radius:12px;padding:14px;margin:12px 0;background:#0f172a}}
pre{{background:#0f172a;border:1px solid #334155;border-radius:12px;padding:12px;white-space:pre-wrap}}
</style></head><body>
<nav><a href="/release-center">Overview</a><a href="/release-center/plan">Plan</a><a href="/release-center/updates">Updates</a><a href="/release-center/channels">Channels</a></nav>
<main>{body}</main></body></html>"""


def render_release_overview() -> str:
    return render_release_shell("Release Center", f"<h1>Release Automation and Update Center</h1><pre>{escape(str(release_center_status()))}</pre>")


def render_release_plan_page() -> str:
    return render_release_shell("Release Plan", f"<h1>Release Plan</h1><pre>{escape(str(release_plan_demo()))}</pre>")


def render_update_page() -> str:
    return render_release_shell("Updates", f"<h1>Update Center</h1><pre>{escape(str(update_plan_demo()))}</pre>")


def render_channels_page() -> str:
    return render_release_shell("Release Channels", f"<h1>Release Channels</h1><pre>{escape(str({'channels': release_channel_manifest(), 'gates': rollback_migration_demo()}))}</pre>")
