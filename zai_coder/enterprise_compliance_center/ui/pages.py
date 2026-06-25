"""Enterprise Compliance Center dashboard pages."""

from __future__ import annotations

from html import escape

from zai_coder.enterprise_compliance_center.control import compliance_center_status, compliance_overview
from zai_coder.enterprise_compliance_center.frameworks import framework_catalog
from zai_coder.enterprise_compliance_center.controls import control_library
from zai_coder.enterprise_compliance_center.risk_matrix import risk_control_matrix


def render_compliance_shell(title: str, body: str) -> str:
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
<nav><a href="/compliance">Overview</a><a href="/compliance/frameworks">Frameworks</a><a href="/compliance/controls">Controls</a><a href="/compliance/risks">Risks</a></nav>
<main>{body}</main></body></html>"""


def render_compliance_overview_page() -> str:
    return render_compliance_shell("Enterprise Compliance Center", f"<h1>Enterprise Compliance Center</h1><pre>{escape(str(compliance_center_status()))}</pre>")


def render_frameworks_page() -> str:
    rows = "\n".join(f"<tr><td>{escape(f['id'])}</td><td>{escape(f['name'])}</td><td>{escape(f['jurisdiction'])}</td></tr>" for f in framework_catalog())
    return render_compliance_shell("Compliance Frameworks", f"<h1>Frameworks</h1><table><tbody>{rows}</tbody></table>")


def render_controls_page() -> str:
    rows = "\n".join(f"<tr><td>{escape(c['id'])}</td><td>{escape(c['framework_id'])}</td><td>{escape(c['title'])}</td><td>{escape(c['status'])}</td></tr>" for c in control_library())
    return render_compliance_shell("Compliance Controls", f"<h1>Controls</h1><table><tbody>{rows}</tbody></table>")


def render_risks_page() -> str:
    return render_compliance_shell("Compliance Risks", f"<h1>Risks</h1><pre>{escape(str(risk_control_matrix()))}</pre>")
