"""Cloudflare go-live UI pages."""

from __future__ import annotations

from html import escape

from zai_coder.cloudflare_go_live.models import CloudflareGoLiveConfig
from zai_coder.cloudflare_go_live.go_live_wizard import go_live_wizard_plan
from zai_coder.cloudflare_go_live.access_policy import access_policy_checklist
from zai_coder.cloudflare_go_live.dns_planner import dns_record_plan, dns_rollback_plan
from zai_coder.cloudflare_go_live.public_health import public_health_verification_plan


def render_cloudflare_shell(title: str, body: str) -> str:
    return f"""<!doctype html><html><head><meta charset="utf-8"><title>{escape(title)}</title>
<style>
body{{font-family:system-ui;background:#020617;color:#e2e8f0;margin:0}}
nav{{background:#0f172a;padding:16px;display:flex;gap:14px}}
a{{color:#7dd3fc;text-decoration:none}}
main{{padding:24px}}
.card{{border:1px solid #334155;border-radius:12px;padding:14px;margin:12px 0;background:#0f172a}}
pre{{background:#0f172a;border:1px solid #334155;padding:12px;border-radius:12px;white-space:pre-wrap}}
</style></head><body>
<nav><a href="/cloudflare">Go-Live</a><a href="/cloudflare/access">Access</a><a href="/cloudflare/dns">DNS</a><a href="/cloudflare/rollback">Rollback</a></nav>
<main>{body}</main></body></html>"""


def render_go_live_page(config: CloudflareGoLiveConfig | None = None) -> str:
    config = config or CloudflareGoLiveConfig()
    plan = go_live_wizard_plan(config)
    steps = "".join(f"<li>{escape(step)}</li>" for step in plan.steps)
    warnings = "".join(f"<li>{escape(w)}</li>" for w in plan.warnings)
    body = f"<h1>Cloudflare Go-Live</h1><div class='card'><h2>{escape(config.hostname)}</h2><ol>{steps}</ol></div><div class='card'><h2>Warnings</h2><ul>{warnings}</ul></div>"
    return render_cloudflare_shell("Cloudflare Go-Live", body)


def render_access_page(config: CloudflareGoLiveConfig | None = None) -> str:
    rows = "".join(f"<li>{escape(item['area'])}: {escape(item['item'])}</li>" for item in access_policy_checklist(config))
    return render_cloudflare_shell("Cloudflare Access", f"<h1>Cloudflare Access Checklist</h1><ul>{rows}</ul>")


def render_dns_page(config: CloudflareGoLiveConfig | None = None) -> str:
    plan = dns_record_plan(config)
    return render_cloudflare_shell("DNS Plan", f"<h1>DNS Plan</h1><pre>{escape(str(plan.to_dict()))}</pre>")


def render_rollback_page(config: CloudflareGoLiveConfig | None = None) -> str:
    plan = dns_rollback_plan(config)
    return render_cloudflare_shell("DNS Rollback", f"<h1>Rollback Plan</h1><pre>{escape(str(plan.to_dict()))}</pre>")


def render_public_health_page(config: CloudflareGoLiveConfig | None = None) -> str:
    plan = public_health_verification_plan(config)
    return render_cloudflare_shell("Public Health", f"<h1>Public Health Verification</h1><pre>{escape(str(plan.to_dict()))}</pre>")
