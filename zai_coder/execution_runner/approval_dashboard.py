"""Human approval dashboard."""

from __future__ import annotations

from html import escape


def render_approval_dashboard(items: list[dict]) -> str:
    rows = "\n".join(
        f"<tr><td>{escape(str(item.get('id','')))}</td><td>{escape(str(item.get('provider','')))}</td><td>{escape(str(item.get('action','')))}</td><td>{escape(str(item.get('status','')))}</td></tr>"
        for item in items
    )
    return f"""<!doctype html><html><head><meta charset="utf-8"><title>Approval Dashboard</title></head><body>
<h1>Human Approval Dashboard</h1>
<p>Apply execution requires approval id with prefix <code>approved_</code>.</p>
<table><tbody>{rows}</tbody></table>
</body></html>
"""


def approval_token_plan(reason: str = "manual-review") -> dict:
    return {
        "dry_run": True,
        "prefix": "approved_",
        "reason": reason,
        "instructions": [
            "review command safety report",
            "review provider env validation",
            "review rollback plan",
            "create approval id out-of-band",
            "set APPROVAL_ID=approved_<unique-id>",
        ],
    }
