"""Document renderers."""

from __future__ import annotations

import html
from .models import DocumentProject


def validate_document(doc: DocumentProject) -> list[str]:
    issues: list[str] = []
    if not doc.title:
        issues.append("missing title")
    if not doc.audience:
        issues.append("missing audience")
    if not doc.purpose:
        issues.append("missing purpose")
    if doc.status not in {"draft", "review", "approved", "published"}:
        issues.append(f"invalid status: {doc.status}")
    seen = set()
    for section in doc.sections:
        key = section.heading.strip().lower()
        if not key:
            issues.append("empty section heading")
        if key in seen:
            issues.append(f"duplicate section: {section.heading}")
        seen.add(key)
    return issues


def render_markdown(doc: DocumentProject) -> str:
    parts = [
        f"# {doc.title}",
        "",
        f"- Audience: {doc.audience}",
        f"- Purpose: {doc.purpose}",
        f"- Status: {doc.status}",
        "",
    ]
    for section in doc.sections:
        parts.append(section.to_markdown())
    return "\n".join(parts).rstrip() + "\n"


def render_html(doc: DocumentProject) -> str:
    md = render_markdown(doc)
    body = "<br>\n".join(html.escape(line) for line in md.splitlines())
    return f"<!doctype html><html><head><meta charset='utf-8'><title>{html.escape(doc.title)}</title></head><body>{body}</body></html>\n"
