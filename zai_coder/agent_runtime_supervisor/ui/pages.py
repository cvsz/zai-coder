"""Agent runtime supervisor dashboard pages."""

from __future__ import annotations

from html import escape

from zai_coder.agent_runtime_supervisor.control import supervisor_status, agent_start_gate
from zai_coder.agent_runtime_supervisor.sandbox import sandbox_profile_manifest
from zai_coder.agent_runtime_supervisor.lifecycle import lifecycle_plan
from zai_coder.agent_runtime_supervisor.heartbeat import heartbeat_policy


def render_agent_shell(title: str, body: str) -> str:
    return f"""<!doctype html><html><head><meta charset="utf-8"><title>{escape(title)}</title>
<style>
body{{font-family:system-ui;background:#020617;color:#e2e8f0;margin:0}}
nav{{background:#0f172a;padding:16px;display:flex;gap:14px}}
a{{color:#7dd3fc;text-decoration:none}}
main{{padding:24px}}
.card{{border:1px solid #334155;border-radius:12px;padding:14px;margin:12px 0;background:#0f172a}}
pre{{background:#0f172a;border:1px solid #334155;border-radius:12px;padding:12px;white-space:pre-wrap}}
</style></head><body>
<nav><a href="/agents">Overview</a><a href="/agents/sandbox">Sandbox</a><a href="/agents/lifecycle">Lifecycle</a><a href="/agents/policy">Policy</a></nav>
<main>{body}</main></body></html>"""


def render_agent_overview() -> str:
    return render_agent_shell("Agent Runtime Supervisor", f"<h1>Agent Runtime Supervisor</h1><pre>{escape(str(supervisor_status()))}</pre>")


def render_agent_sandbox_page() -> str:
    return render_agent_shell("Agent Sandbox", f"<h1>Sandbox Profiles</h1><pre>{escape(str(sandbox_profile_manifest()))}</pre>")


def render_agent_lifecycle_page() -> str:
    return render_agent_shell("Agent Lifecycle", f"<h1>Lifecycle</h1><pre>{escape(str({'start': lifecycle_plan('start'), 'recover': lifecycle_plan('recover')}))}</pre>")


def render_agent_policy_page() -> str:
    return render_agent_shell("Agent Policy", f"<h1>Agent Policy</h1><pre>{escape(str({'heartbeat': heartbeat_policy(), 'start_gate': agent_start_gate()}))}</pre>")
