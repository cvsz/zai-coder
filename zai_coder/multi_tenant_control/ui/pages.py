"""Admin tenant dashboard pages."""

from __future__ import annotations

from html import escape

from zai_coder.multi_tenant_control.onboarding import tenant_onboarding_plan
from zai_coder.multi_tenant_control.migration import tenant_migration_plan
from zai_coder.multi_tenant_control.backup_export import tenant_backup_policy


def render_tenant_shell(title: str, body: str) -> str:
    return f"""<!doctype html><html><head><meta charset="utf-8"><title>{escape(title)}</title>
<style>
body{{font-family:system-ui;background:#020617;color:#e2e8f0;margin:0}}
nav{{background:#0f172a;padding:16px;display:flex;gap:14px}}
a{{color:#7dd3fc;text-decoration:none}}
main{{padding:24px}}
.card{{border:1px solid #334155;border-radius:12px;padding:14px;margin:12px 0;background:#0f172a}}
pre{{background:#0f172a;border:1px solid #334155;border-radius:12px;padding:12px;white-space:pre-wrap}}
</style></head><body>
<nav><a href="/tenants">Overview</a><a href="/tenants/onboarding">Onboarding</a><a href="/tenants/backup">Backup</a><a href="/tenants/migration">Migration</a></nav>
<main>{body}</main></body></html>"""


def render_tenant_overview() -> str:
    body = """
<h1>Multi-Tenant Control</h1>
<div class="card"><h2>Isolation</h2><p>Org/workspace runtime isolation and access guard.</p></div>
<div class="card"><h2>API Keys</h2><p>Tenant-scoped API keys with workspace scopes.</p></div>
<div class="card"><h2>Audit</h2><p>Tenant-scoped audit trails.</p></div>
<div class="card"><h2>Quota</h2><p>Workspace quota enforcement.</p></div>
"""
    return render_tenant_shell("Multi-Tenant Control", body)


def render_onboarding_page() -> str:
    return render_tenant_shell("Tenant Onboarding", f"<h1>Tenant Onboarding</h1><pre>{escape(str(tenant_onboarding_plan()))}</pre>")


def render_backup_page() -> str:
    return render_tenant_shell("Tenant Backup", f"<h1>Tenant Backup</h1><pre>{escape(str(tenant_backup_policy()))}</pre>")


def render_migration_page() -> str:
    return render_tenant_shell("Tenant Migration", f"<h1>Tenant Migration</h1><pre>{escape(str(tenant_migration_plan()))}</pre>")
