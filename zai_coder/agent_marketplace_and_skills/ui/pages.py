"""Marketplace dashboard pages."""

from __future__ import annotations

from html import escape

from zai_coder.agent_marketplace_and_skills.control import marketplace_overview, marketplace_status
from zai_coder.agent_marketplace_and_skills.catalog import skill_catalog, agent_catalog
from zai_coder.agent_marketplace_and_skills.install_policy import install_policy_decision


def render_marketplace_shell(title: str, body: str) -> str:
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
<nav><a href="/marketplace">Overview</a><a href="/marketplace/skills">Skills</a><a href="/marketplace/agents">Agents</a><a href="/marketplace/policy">Policy</a></nav>
<main>{body}</main></body></html>"""


def render_marketplace_overview() -> str:
    return render_marketplace_shell("Agent Marketplace", f"<h1>Agent Marketplace and Skills</h1><pre>{escape(str(marketplace_status()))}</pre>")


def render_skills_page() -> str:
    rows = "\n".join(f"<tr><td>{escape(s['id'])}</td><td>{escape(s['name'])}</td><td>{escape(s['version'])}</td><td>{escape(s['category'])}</td></tr>" for s in skill_catalog())
    return render_marketplace_shell("Skills", f"<h1>Skills</h1><table><tbody>{rows}</tbody></table>")


def render_agents_page() -> str:
    rows = "\n".join(f"<tr><td>{escape(a['id'])}</td><td>{escape(a['name'])}</td><td>{escape(a['agent_type'])}</td><td>{escape(', '.join(a['default_skills']))}</td></tr>" for a in agent_catalog())
    return render_marketplace_shell("Agents", f"<h1>Agents</h1><table><tbody>{rows}</tbody></table>")


def render_policy_page() -> str:
    policy = install_policy_decision("repo-planner", "builder", ("tenant_admin",), True, "", False)
    return render_marketplace_shell("Marketplace Policy", f"<h1>Policy</h1><pre>{escape(str(policy))}</pre>")
