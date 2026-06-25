"""Unified App Studio dashboard renderer."""

from __future__ import annotations

from html import escape
from typing import Iterable


def render_app_studio_dashboard(
    projects: Iterable[dict],
    members: Iterable[dict],
    plans: Iterable[dict],
    runs: Iterable[dict],
    audit_events: Iterable[dict],
) -> str:
    def rows(items, fields):
        return "\n".join(
            "<tr>" + "".join(f"<td>{escape(str(item.get(field, '')))}</td>" for field in fields) + "</tr>"
            for item in items
        )

    project_rows = rows(projects, ["slug", "title", "project_type", "status"])
    member_rows = rows(members, ["email", "display_name", "status"])
    plan_rows = rows(plans, ["slug", "name", "monthly_price_cents"])
    run_rows = rows(runs, ["id", "run_type", "status"])
    audit_rows = rows(audit_events, ["actor", "action", "target"])

    return f"""<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>ZAI App Studio</title>
  <style>
    body {{ font-family: system-ui, sans-serif; background: #020617; color: #e2e8f0; margin: 0; }}
    main {{ max-width: 1180px; margin: 0 auto; padding: 32px; }}
    section {{ border: 1px solid #334155; border-radius: 16px; background: #0f172a; padding: 18px; margin: 18px 0; }}
    table {{ border-collapse: collapse; width: 100%; }}
    th, td {{ border: 1px solid #334155; padding: 8px; text-align: left; }}
    th {{ background: #1e293b; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 18px; }}
  </style>
</head>
<body>
<main>
  <h1>ZAI App Studio</h1>
  <p>Unified local-first admin dashboard for workspaces, members, billing, creative projects, runs, and audit logs.</p>
  <div class="grid">
    <section><h2>Projects</h2><table><tbody>{project_rows}</tbody></table></section>
    <section><h2>Members</h2><table><tbody>{member_rows}</tbody></table></section>
    <section><h2>Plans</h2><table><tbody>{plan_rows}</tbody></table></section>
    <section><h2>Runs</h2><table><tbody>{run_rows}</tbody></table></section>
  </div>
  <section><h2>Audit</h2><table><tbody>{audit_rows}</tbody></table></section>
</main>
</body>
</html>
"""
