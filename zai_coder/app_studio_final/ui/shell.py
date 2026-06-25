"""Final App Studio HTML shell."""

from __future__ import annotations

from html import escape


NAV_ITEMS = [
    ("Dashboard", "/"),
    ("Projects", "/studio/projects"),
    ("Plugins", "/studio/plugins"),
    ("Workflows", "/studio/workflows"),
    ("Models", "/studio/models"),
    ("Deployments", "/studio/deployments"),
    ("Billing", "/saas/billing"),
    ("Usage", "/saas/usage"),
    ("Audit", "/saas/audit"),
    ("Settings", "/saas/settings"),
]


def render_shell(title: str, body: str, active: str = "Dashboard") -> str:
    nav = "\n".join(
        f"<a class='nav-item {'active' if label == active else ''}' href='{escape(href)}'>{escape(label)}</a>"
        for label, href in NAV_ITEMS
    )
    return f"""<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>{escape(title)}</title>
  <style>
    :root {{ color-scheme: dark; font-family: Inter, system-ui, sans-serif; }}
    body {{ margin: 0; background: #020617; color: #e2e8f0; }}
    .layout {{ display: grid; grid-template-columns: 260px 1fr; min-height: 100vh; }}
    aside {{ background: #0f172a; border-right: 1px solid #334155; padding: 24px; }}
    main {{ padding: 32px; max-width: 1280px; }}
    .brand {{ font-size: 20px; font-weight: 800; margin-bottom: 24px; }}
    .nav-item {{ display:block; color:#cbd5e1; text-decoration:none; padding:10px 12px; border-radius:10px; margin:4px 0; }}
    .nav-item.active, .nav-item:hover {{ background:#1e293b; color:#7dd3fc; }}
    .grid {{ display:grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap:18px; }}
    .card {{ border:1px solid #334155; background:#0f172a; border-radius:16px; padding:18px; }}
    table {{ width:100%; border-collapse:collapse; }}
    th,td {{ border:1px solid #334155; padding:8px; text-align:left; }}
    th {{ background:#1e293b; }}
    .badge {{ display:inline-block; border:1px solid #38bdf8; color:#7dd3fc; border-radius:999px; padding:3px 9px; font-size:12px; }}
  </style>
</head>
<body>
  <div class="layout">
    <aside>
      <div class="brand">ZAI App Studio</div>
      {nav}
    </aside>
    <main>
      {body}
    </main>
  </div>
</body>
</html>
"""
