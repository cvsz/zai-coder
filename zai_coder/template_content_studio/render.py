"""Safe local template rendering."""

from __future__ import annotations

import html
import uuid

from .models import RenderedContent
from .templates import template_by_id
from .variables import validate_render_variables, VARIABLE_RE
from .brand import content_safety_gate


def render_template(template_id: str, variables: dict) -> RenderedContent:
    template = template_by_id(template_id)
    validation = validate_render_variables(template.to_dict(), variables)
    if not validation["ok"]:
        raise ValueError(f"invalid render variables: {validation}")
    def replace(match):
        key = match.group(1)
        return str(variables.get(key, ""))
    content = VARIABLE_RE.sub(replace, template.body)
    rendered = RenderedContent(
        id=f"cnt_{uuid.uuid4().hex[:12]}",
        template_id=template.id,
        title=template.title,
        content=content,
        channel=template.channel,
        variables=variables,
    )
    issues = rendered.validate()
    if issues:
        raise ValueError("; ".join(issues))
    return rendered


def render_html_preview(rendered: RenderedContent | dict) -> str:
    payload = rendered.to_dict() if hasattr(rendered, "to_dict") else rendered
    escaped = html.escape(payload["content"]).replace("\n", "<br>")
    return f"<article><h1>{html.escape(payload['title'])}</h1><div>{escaped}</div></article>"


def render_demo_content() -> dict:
    rendered = render_template(
        "tpl-welcome-email",
        {
            "customer_name": "Demo Customer",
            "product_name": "ZAI Coder Control Plane",
            "workspace_name": "Demo Workspace",
            "next_step": "review the local-first onboarding checklist",
        },
    )
    return {"rendered": rendered.to_dict(), "safety": content_safety_gate(rendered.to_dict()), "html": render_html_preview(rendered)}
