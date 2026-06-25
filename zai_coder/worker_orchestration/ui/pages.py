"""Worker orchestration dashboard pages."""

from __future__ import annotations

from html import escape

from zai_coder.worker_orchestration.control import orchestrator_status
from zai_coder.worker_orchestration.scheduler import schedule_manifest
from zai_coder.worker_orchestration.concurrency import queue_concurrency_policy


def render_worker_shell(title: str, body: str) -> str:
    return f"""<!doctype html><html><head><meta charset="utf-8"><title>{escape(title)}</title>
<style>
body{{font-family:system-ui;background:#020617;color:#e2e8f0;margin:0}}
nav{{background:#0f172a;padding:16px;display:flex;gap:14px}}
a{{color:#7dd3fc;text-decoration:none}}
main{{padding:24px}}
.card{{border:1px solid #334155;border-radius:12px;padding:14px;margin:12px 0;background:#0f172a}}
pre{{background:#0f172a;border:1px solid #334155;border-radius:12px;padding:12px;white-space:pre-wrap}}
</style></head><body>
<nav><a href="/workers">Overview</a><a href="/workers/schedules">Schedules</a><a href="/workers/policy">Policy</a></nav>
<main>{body}</main></body></html>"""


def render_worker_overview() -> str:
    return render_worker_shell("Worker Orchestration", f"<h1>Worker Orchestration</h1><pre>{escape(str(orchestrator_status()))}</pre>")


def render_schedules_page() -> str:
    return render_worker_shell("Worker Schedules", f"<h1>Schedules</h1><pre>{escape(str(schedule_manifest()))}</pre>")


def render_worker_policy_page() -> str:
    return render_worker_shell("Worker Policy", f"<h1>Worker Policy</h1><pre>{escape(str(queue_concurrency_policy()))}</pre>")
