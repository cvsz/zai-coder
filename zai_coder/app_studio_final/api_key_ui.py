"""API key management UI helpers."""

from __future__ import annotations

from html import escape


def render_api_keys_page(keys: list[dict]) -> str:
    rows = "\n".join(
        f"<tr><td>{escape(str(k.get('name','')))}</td><td>{escape(str(k.get('prefix','')))}</td><td>{escape(str(k.get('status','')))}</td></tr>"
        for k in keys
    )
    return f"""<!doctype html><html><head><meta charset='utf-8'><title>API Keys</title></head><body>
<h1>API Keys</h1>
<p>Raw keys are shown only once at creation time. Never commit keys.</p>
<table><tbody>{rows}</tbody></table>
</body></html>
"""
