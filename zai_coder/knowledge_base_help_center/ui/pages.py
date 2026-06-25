"""Knowledge Base and Help Center UI pages."""

from __future__ import annotations

from html import escape

from zai_coder.knowledge_base_help_center.control import help_center_status
from zai_coder.knowledge_base_help_center.articles import article_by_visibility
from zai_coder.knowledge_base_help_center.faq import faq_catalog
from zai_coder.knowledge_base_help_center.search import help_search


def render_help_shell(title: str, body: str) -> str:
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
<nav><a href="/help">Overview</a><a href="/help/articles">Articles</a><a href="/help/faq">FAQ</a><a href="/help/search">Search</a><a href="/help/admin">Admin View</a></nav>
<main>{body}</main></body></html>"""


def render_help_overview_page() -> str:
    return render_help_shell("Knowledge Base and Help Center", f"<h1>Knowledge Base and Help Center</h1><pre>{escape(str(help_center_status()))}</pre>")


def render_articles_page() -> str:
    rows = "\n".join(f"<tr><td>{escape(a['title'])}</td><td>{escape(a['category'])}</td><td>{escape(a['visibility'])}</td></tr>" for a in article_by_visibility("customer"))
    return render_help_shell("Help Articles", f"<h1>Articles</h1><table><tbody>{rows}</tbody></table>")


def render_faq_page() -> str:
    rows = "\n".join(f"<tr><td>{escape(f['question'])}</td><td>{escape(f['category'])}</td></tr>" for f in faq_catalog())
    return render_help_shell("FAQ", f"<h1>FAQ</h1><table><tbody>{rows}</tbody></table>")


def render_search_page() -> str:
    return render_help_shell("Help Search", f"<h1>Search</h1><pre>{escape(str(help_search('billing charge')))}</pre>")


def render_admin_help_page() -> str:
    rows = "\n".join(f"<tr><td>{escape(a['title'])}</td><td>{escape(a['audience'])}</td><td>{escape(a['visibility'])}</td><td>{escape(a['status'])}</td></tr>" for a in article_by_visibility("private"))
    return render_help_shell("Admin Help View", f"<h1>Admin View</h1><table><tbody>{rows}</tbody></table>")
