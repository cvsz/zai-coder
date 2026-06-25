"""Execution audit timeline renderer."""

from __future__ import annotations

from html import escape


def render_execution_timeline(events: list[dict]) -> str:
    rows = "\n".join(
        f"<tr><td>{escape(str(e.get('created_at','')))}</td><td>{escape(str(e.get('provider','')))}</td><td>{escape(str(e.get('action','')))}</td><td>{escape(str(e.get('status','')))}</td><td>{escape(str(e.get('returncode','')))}</td></tr>"
        for e in events
    )
    return f"""<!doctype html><html><head><meta charset="utf-8"><title>Execution Timeline</title></head><body>
<h1>Execution Audit Timeline</h1>
<table><tbody>{rows}</tbody></table>
</body></html>
"""
