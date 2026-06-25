"""Gateway dashboard pages."""

from __future__ import annotations

from html import escape

from zai_coder.production_api_gateway.router import route_manifest
from zai_coder.production_api_gateway.upstreams import upstream_manifest
from zai_coder.production_api_gateway.rate_limit import rate_limit_policy_manifest
from zai_coder.production_api_gateway.deploy import gateway_deploy_plan


def render_gateway_shell(title: str, body: str) -> str:
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
<nav><a href="/gateway">Overview</a><a href="/gateway/routes">Routes</a><a href="/gateway/upstreams">Upstreams</a><a href="/gateway/security">Security</a></nav>
<main>{body}</main></body></html>"""


def render_gateway_overview() -> str:
    body = """
<h1>Production API Gateway</h1>
<div class="card"><h2>Routing</h2><p>Gateway route registry and upstream service manifest.</p></div>
<div class="card"><h2>Security</h2><p>Tenant-aware auth, API-key guard, security headers, and CORS.</p></div>
<div class="card"><h2>Rate Limits</h2><p>In-memory policy scaffold for standard, strict, and admin paths.</p></div>
<div class="card"><h2>Audit</h2><p>Gateway audit hook for request/response metadata.</p></div>
"""
    return render_gateway_shell("Production API Gateway", body)


def render_routes_page() -> str:
    rows = "\n".join(f"<tr><td>{escape(r['method'])}</td><td>{escape(r['path'])}</td><td>{escape(r['upstream'])}</td><td>{r['auth_required']}</td><td>{r['tenant_required']}</td></tr>" for r in route_manifest())
    return render_gateway_shell("Gateway Routes", f"<h1>Gateway Routes</h1><table><tbody>{rows}</tbody></table>")


def render_upstreams_page() -> str:
    rows = "\n".join(f"<tr><td>{escape(u['id'])}</td><td>{escape(u['name'])}</td><td>{escape(u['base_url'])}</td></tr>" for u in upstream_manifest())
    return render_gateway_shell("Upstreams", f"<h1>Upstreams</h1><table><tbody>{rows}</tbody></table>")


def render_security_page() -> str:
    payload = {"rate_limits": rate_limit_policy_manifest(), "deploy": gateway_deploy_plan()}
    return render_gateway_shell("Gateway Security", f"<h1>Gateway Security</h1><pre>{escape(str(payload))}</pre>")
