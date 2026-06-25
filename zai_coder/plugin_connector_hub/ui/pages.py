"""Connector Hub dashboard pages."""

from __future__ import annotations

from html import escape

from zai_coder.plugin_connector_hub.control import connector_hub_status
from zai_coder.plugin_connector_hub.catalog import connector_catalog
from zai_coder.plugin_connector_hub.install_policy import install_policy_decision
from zai_coder.plugin_connector_hub.sync import sync_schedule_policy


def render_connector_shell(title: str, body: str) -> str:
    return f"""<!doctype html><html><head><meta charset="utf-8"><title>{escape(title)}</title>
<style>
body{{font-family:system-ui;background:#020617;color:#e2e8f0;margin:0}}
nav{{background:#0f172a;padding:16px;display:flex;gap:14px}}
a{{color:#7dd3fc;text-decoration:none}}
main{{padding:24px}}
.card{{border:1px solid #334155;border-radius:12px;padding:14px;margin:12px 0;background:#0f172a}}
table{{width:100%;border-collapse:collapse}}td,th{{border:1px solid #334155;padding:8px}}
pre{{background:#0f172a;border:1px solid #334155;border-radius:12px;padding:12px;white-space:pre-wrap}}
</style></head><body>
<nav><a href="/connectors">Overview</a><a href="/connectors/catalog">Catalog</a><a href="/connectors/policy">Policy</a><a href="/connectors/sync">Sync</a></nav>
<main>{body}</main></body></html>"""


def render_connector_overview() -> str:
    return render_connector_shell("Plugin Connector Hub", f"<h1>Plugin Connector Hub</h1><pre>{escape(str(connector_hub_status()))}</pre>")


def render_connector_catalog_page() -> str:
    rows = "\n".join(f"<tr><td>{escape(c['id'])}</td><td>{escape(c['name'])}</td><td>{escape(c['category'])}</td><td>{escape(', '.join(c['supported_actions']))}</td></tr>" for c in connector_catalog())
    return render_connector_shell("Connector Catalog", f"<h1>Connector Catalog</h1><table><tbody>{rows}</tbody></table>")


def render_connector_policy_page() -> str:
    policy = install_policy_decision("github", ("tenant_admin",), {}, True, "", False)
    return render_connector_shell("Connector Policy", f"<h1>Connector Policy</h1><pre>{escape(str(policy))}</pre>")


def render_connector_sync_page() -> str:
    return render_connector_shell("Connector Sync", f"<h1>Connector Sync</h1><pre>{escape(str(sync_schedule_policy()))}</pre>")
