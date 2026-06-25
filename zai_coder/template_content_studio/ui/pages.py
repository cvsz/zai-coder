"""Template and Content Studio UI pages."""

from __future__ import annotations

from html import escape

from zai_coder.template_content_studio.control import content_studio_status, content_studio_overview
from zai_coder.template_content_studio.templates import template_registry
from zai_coder.template_content_studio.render import render_demo_content
from zai_coder.template_content_studio.brand import brand_rules


def render_content_shell(title: str, body: str) -> str:
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
<nav><a href="/content-studio">Overview</a><a href="/content-studio/templates">Templates</a><a href="/content-studio/render">Render</a><a href="/content-studio/brand">Brand</a><a href="/content-studio/library">Library</a></nav>
<main>{body}</main></body></html>"""


def render_content_overview_page() -> str:
    return render_content_shell("Template and Content Studio", f"<h1>Template and Content Studio</h1><pre>{escape(str(content_studio_status()))}</pre>")


def render_templates_page() -> str:
    rows = "\n".join(f"<tr><td>{escape(t['title'])}</td><td>{escape(t['template_type'])}</td><td>{escape(t['visibility'])}</td></tr>" for t in template_registry())
    return render_content_shell("Content Templates", f"<h1>Templates</h1><table><tbody>{rows}</tbody></table>")


def render_render_page() -> str:
    demo = render_demo_content()
    return render_content_shell("Rendered Content", f"<h1>Render Demo</h1><pre>{escape(demo['rendered']['content'])}</pre>")


def render_brand_page() -> str:
    return render_content_shell("Brand Rules", f"<h1>Brand Rules</h1><pre>{escape(str(brand_rules()))}</pre>")


def render_library_page() -> str:
    overview = content_studio_overview()
    return render_content_shell("Content Library", f"<h1>Library</h1><pre>{escape(str({'templates': len(overview['templates']), 'customer_templates': len(overview['customer_templates'])}))}</pre>")
