"""Self-healing operations dashboard pages."""

from __future__ import annotations

from html import escape

from zai_coder.self_healing_operations.control import self_healing_status, self_healing_overview, healing_plan_demo
from zai_coder.self_healing_operations.playbooks import playbook_catalog
from zai_coder.self_healing_operations.escalation import escalation_policy


def render_healing_shell(title: str, body: str) -> str:
    return f"""<!doctype html><html><head><meta charset="utf-8"><title>{escape(title)}</title>
<style>
body{{font-family:system-ui;background:#020617;color:#e2e8f0;margin:0}}
nav{{background:#0f172a;padding:16px;display:flex;gap:14px}}
a{{color:#7dd3fc;text-decoration:none}}
main{{padding:24px}}
.card{{border:1px solid #334155;border-radius:12px;padding:14px;margin:12px 0;background:#0f172a}}
pre{{background:#0f172a;border:1px solid #334155;border-radius:12px;padding:12px;white-space:pre-wrap}}
</style></head><body>
<nav><a href="/self-healing">Overview</a><a href="/self-healing/incidents">Incidents</a><a href="/self-healing/playbooks">Playbooks</a><a href="/self-healing/policy">Policy</a></nav>
<main>{body}</main></body></html>"""


def render_healing_overview() -> str:
    return render_healing_shell("Self-Healing Operations", f"<h1>Self-Healing Operations</h1><pre>{escape(str(self_healing_status()))}</pre>")


def render_incidents_page() -> str:
    return render_healing_shell("Incidents", f"<h1>Incidents</h1><pre>{escape(str(self_healing_overview()))}</pre>")


def render_playbooks_page() -> str:
    return render_healing_shell("Playbooks", f"<h1>Playbooks</h1><pre>{escape(str(playbook_catalog()))}</pre>")


def render_policy_page() -> str:
    return render_healing_shell("Self-Healing Policy", f"<h1>Policy</h1><pre>{escape(str({'escalation': escalation_policy()}))}</pre>")
