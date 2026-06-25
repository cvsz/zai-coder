"""Enterprise Reporting and Board Pack dashboard pages."""

from __future__ import annotations

from html import escape

from zai_coder.enterprise_reporting_board_pack.control import reporting_status, reporting_overview
from zai_coder.enterprise_reporting_board_pack.kpis import kpi_scorecard
from zai_coder.enterprise_reporting_board_pack.decisions import decision_register, risk_register


def render_reporting_shell(title: str, body: str) -> str:
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
<nav><a href="/board-pack">Overview</a><a href="/board-pack/kpis">KPIs</a><a href="/board-pack/decisions">Decisions</a><a href="/board-pack/risks">Risks</a></nav>
<main>{body}</main></body></html>"""


def render_board_overview_page() -> str:
    return render_reporting_shell("Enterprise Reporting and Board Pack", f"<h1>Enterprise Reporting and Board Pack</h1><pre>{escape(str(reporting_status()))}</pre>")


def render_kpis_page() -> str:
    rows = "\n".join(f"<tr><td>{escape(k['name'])}</td><td>{k['value']}</td><td>{escape(k['unit'])}</td><td>{escape(k['status'])}</td></tr>" for k in kpi_scorecard()["scorecard"])
    return render_reporting_shell("Board KPIs", f"<h1>KPIs</h1><table><tbody>{rows}</tbody></table>")


def render_decisions_page() -> str:
    rows = "\n".join(f"<tr><td>{escape(d['title'])}</td><td>{escape(d['owner'])}</td><td>{escape(d['status'])}</td></tr>" for d in decision_register())
    return render_reporting_shell("Board Decisions", f"<h1>Decisions</h1><table><tbody>{rows}</tbody></table>")


def render_risks_page() -> str:
    rows = "\n".join(f"<tr><td>{escape(r['title'])}</td><td>{escape(r['severity'])}</td><td>{escape(r['status'])}</td><td>{escape(r['mitigation'])}</td></tr>" for r in risk_register())
    return render_reporting_shell("Board Risks", f"<h1>Risks</h1><table><tbody>{rows}</tbody></table>")
