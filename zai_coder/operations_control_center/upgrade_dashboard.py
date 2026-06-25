"""Upgrade and rollback dashboard plans."""

from __future__ import annotations

from html import escape

from zai_coder.deploy_installer_core.upgrade_rollback import upgrade_plan, rollback_plan


def render_upgrade_dashboard(version: str = "v0.15.0") -> str:
    plan = upgrade_plan(version)
    commands = "\n".join(escape(cmd) for cmd in plan["commands"])
    return f"""<!doctype html><html><head><meta charset="utf-8"><title>Upgrade Dashboard</title></head><body>
<h1>Upgrade Dashboard</h1>
<p>Version: {escape(version)}</p>
<pre>{commands}</pre>
</body></html>
"""


def upgrade_action_plan(version: str = "v0.15.0") -> dict:
    return upgrade_plan(version)


def rollback_action_plan(version: str = "v0.14.0") -> dict:
    return rollback_plan(version)
