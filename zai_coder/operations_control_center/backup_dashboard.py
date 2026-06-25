"""Backup and restore dashboard plans."""

from __future__ import annotations

from html import escape

from zai_coder.deploy_installer_core.backup_restore import backup_plan, restore_plan


def render_backup_dashboard() -> str:
    plan = backup_plan()
    commands = "\n".join(escape(cmd) for cmd in plan["commands"])
    return f"""<!doctype html><html><head><meta charset="utf-8"><title>Backup Dashboard</title></head><body>
<h1>Backup Dashboard</h1>
<p>Dry run: {plan["dry_run"]}</p>
<pre>{commands}</pre>
</body></html>
"""


def backup_action_plan() -> dict:
    return backup_plan()


def restore_action_plan(archive: str) -> dict:
    return restore_plan(archive)
