"""Enterprise governance dashboard pages."""

from __future__ import annotations

from html import escape

from zai_coder.enterprise_governance.policy_engine import policy_manifest
from zai_coder.enterprise_governance.role_matrix import role_matrix_manifest
from zai_coder.enterprise_governance.compliance import compliance_checklist
from zai_coder.enterprise_governance.risk_register import risk_register
from zai_coder.enterprise_governance.release_gate import release_readiness_gate, sample_release_status


def render_governance_shell(title: str, body: str) -> str:
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
<nav><a href="/governance">Overview</a><a href="/governance/policies">Policies</a><a href="/governance/roles">Roles</a><a href="/governance/risks">Risks</a><a href="/governance/release">Release Gate</a></nav>
<main>{body}</main></body></html>"""


def render_governance_overview() -> str:
    body = """
<h1>Enterprise Governance</h1>
<div class="card"><h2>Policy Engine</h2><p>Controls dry-run, approval, secret scan, and public exposure requirements.</p></div>
<div class="card"><h2>Compliance</h2><p>Operational compliance checklist and evidence bundle.</p></div>
<div class="card"><h2>Risk</h2><p>Risk register and mitigation tracking.</p></div>
<div class="card"><h2>Release Gate</h2><p>Readiness decision before production release.</p></div>
"""
    return render_governance_shell("Enterprise Governance", body)


def render_policies_page() -> str:
    rows = "\n".join(f"<tr><td>{escape(p['id'])}</td><td>{escape(p['name'])}</td><td>{escape(p['severity'])}</td></tr>" for p in policy_manifest())
    return render_governance_shell("Policies", f"<h1>Policies</h1><table><tbody>{rows}</tbody></table>")


def render_roles_page() -> str:
    rows = "\n".join(f"<tr><td>{escape(role)}</td><td>{escape(', '.join(perms))}</td></tr>" for role, perms in role_matrix_manifest().items())
    return render_governance_shell("Roles", f"<h1>Role Matrix</h1><table><tbody>{rows}</tbody></table>")


def render_risks_page() -> str:
    rows = "\n".join(f"<tr><td>{escape(r['id'])}</td><td>{escape(r['title'])}</td><td>{r['score']}</td><td>{escape(r['status'])}</td></tr>" for r in risk_register())
    return render_governance_shell("Risk Register", f"<h1>Risk Register</h1><table><tbody>{rows}</tbody></table>")


def render_release_gate_page() -> str:
    gate = release_readiness_gate(sample_release_status())
    return render_governance_shell("Release Gate", f"<h1>Release Readiness Gate</h1><pre>{escape(str(gate))}</pre>")


def render_compliance_page() -> str:
    rows = "\n".join(f"<tr><td>{escape(i['id'])}</td><td>{escape(i['area'])}</td><td>{escape(i['item'])}</td></tr>" for i in compliance_checklist())
    return render_governance_shell("Compliance", f"<h1>Compliance Checklist</h1><table><tbody>{rows}</tbody></table>")
