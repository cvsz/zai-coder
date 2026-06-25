"""Operations Control Center UI pages."""

from __future__ import annotations

from html import escape

from zai_coder.operations_control_center.service_status import default_service_statuses
from zai_coder.operations_control_center.health_dashboard import render_health_dashboard
from zai_coder.operations_control_center.backup_dashboard import render_backup_dashboard
from zai_coder.operations_control_center.upgrade_dashboard import render_upgrade_dashboard


def render_ops_shell(title: str, body: str) -> str:
    nav = """
<a href="/ops">Overview</a>
<a href="/ops/health">Health</a>
<a href="/ops/services">Services</a>
<a href="/ops/logs">Logs</a>
<a href="/ops/backup">Backup</a>
<a href="/ops/upgrade">Upgrade</a>
"""
    return f"""<!doctype html><html><head><meta charset="utf-8"><title>{escape(title)}</title>
<style>
body{{font-family:system-ui;background:#020617;color:#e2e8f0;margin:0}}
nav{{background:#0f172a;padding:16px;display:flex;gap:14px}}
a{{color:#7dd3fc;text-decoration:none}}
main{{padding:24px}}
.card{{border:1px solid #334155;border-radius:12px;padding:14px;margin:12px 0;background:#0f172a}}
table{{width:100%;border-collapse:collapse}}td,th{{border:1px solid #334155;padding:8px}}
</style></head><body><nav>{nav}</nav><main>{body}</main></body></html>"""


def render_ops_overview() -> str:
    cards = """
<div class="card"><h2>Deploy</h2><p>Local, Docker, systemd, and Cloudflare deployment control.</p></div>
<div class="card"><h2>Health</h2><p>Health, readiness, auth, backup, and exposure signals.</p></div>
<div class="card"><h2>Operations</h2><p>Backup, restore, upgrade, rollback, logs, and status plans.</p></div>
"""
    return render_ops_shell("Operations Control Center", f"<h1>Operations Control Center</h1>{cards}")


def render_services_page() -> str:
    rows = "\n".join(
        f"<tr><td>{escape(s.name)}</td><td>{escape(s.target)}</td><td>{escape(s.status)}</td><td>{escape(s.detail)}</td></tr>"
        for s in default_service_statuses()
    )
    body = f"<h1>Service Status</h1><table><tbody>{rows}</tbody></table>"
    return render_ops_shell("Service Status", body)


def render_health_page() -> str:
    return render_ops_shell("Health", render_health_dashboard())


def render_backup_page() -> str:
    return render_ops_shell("Backup", render_backup_dashboard())


def render_upgrade_page() -> str:
    return render_ops_shell("Upgrade", render_upgrade_dashboard())
