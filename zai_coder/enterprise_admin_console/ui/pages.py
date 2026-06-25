"""Enterprise Admin Console dashboard pages."""

from __future__ import annotations

from html import escape

from zai_coder.enterprise_admin_console.control import admin_console_status
from zai_coder.enterprise_admin_console.directory import tenant_directory, workspace_directory, user_directory
from zai_coder.enterprise_admin_console.feature_flags import feature_flag_catalog
from zai_coder.enterprise_admin_console.service_control import service_catalog


def render_admin_shell(title: str, body: str) -> str:
    return f"""<!doctype html><html><head><meta charset="utf-8"><title>{escape(title)}</title>
<style>
body{{font-family:system-ui;background:#020617;color:#e2e8f0;margin:0}}
nav{{background:#0f172a;padding:16px;display:flex;gap:14px;flex-wrap:wrap}}
a{{color:#7dd3fc;text-decoration:none}}
main{{padding:24px}}
.card{{border:1px solid #334155;border-radius:12px;padding:14px;margin:12px 0;background:#0f172a}}
table{{width:100%;border-collapse:collapse}}td,th{{border:1px solid #334155;padding:8px}}
pre{{background:#0f172a;border:1px solid #334155;border-radius:12px;padding:12px;white-space:pre-wrap}}
</style></head><body>
<nav><a href="/admin">Overview</a><a href="/admin/tenants">Tenants</a><a href="/admin/users">Users</a><a href="/admin/flags">Flags</a><a href="/admin/services">Services</a></nav>
<main>{body}</main></body></html>"""


def render_admin_overview_page() -> str:
    return render_admin_shell("Enterprise Admin Console", f"<h1>Enterprise Admin Console</h1><pre>{escape(str(admin_console_status()))}</pre>")


def render_tenants_page() -> str:
    rows = "\n".join(f"<tr><td>{escape(t['id'])}</td><td>{escape(t['name'])}</td><td>{escape(t['plan'])}</td><td>{escape(t['status'])}</td></tr>" for t in tenant_directory())
    return render_admin_shell("Tenants", f"<h1>Tenants</h1><table><tbody>{rows}</tbody></table>")


def render_users_page() -> str:
    rows = "\n".join(f"<tr><td>{escape(u['email'])}</td><td>{escape(u['display_name'])}</td><td>{escape(', '.join(u['roles']))}</td><td>{escape(u['status'])}</td></tr>" for u in user_directory())
    return render_admin_shell("Users", f"<h1>Users</h1><table><tbody>{rows}</tbody></table>")


def render_flags_page() -> str:
    rows = "\n".join(f"<tr><td>{escape(f['id'])}</td><td>{escape(f['name'])}</td><td>{f['enabled']}</td><td>{escape(f['scope'])}</td></tr>" for f in feature_flag_catalog())
    return render_admin_shell("Feature Flags", f"<h1>Feature Flags</h1><table><tbody>{rows}</tbody></table>")


def render_services_page() -> str:
    rows = "\n".join(f"<tr><td>{escape(s['id'])}</td><td>{escape(s['name'])}</td><td>{escape(s['status'])}</td></tr>" for s in service_catalog())
    return render_admin_shell("Services", f"<h1>Services</h1><table><tbody>{rows}</tbody></table>")
