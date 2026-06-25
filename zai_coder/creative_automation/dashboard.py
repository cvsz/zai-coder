"""Static creative dashboard renderer."""

from __future__ import annotations

from html import escape
from typing import Iterable

from .project_types import CreativeProject
from .asset_library import CreativeAsset


def render_creative_dashboard(projects: Iterable[CreativeProject], assets: Iterable[CreativeAsset]) -> str:
    project_rows = "\n".join(
        f"<tr><td>{escape(p.slug)}</td><td>{escape(p.title)}</td><td>{escape(p.project_type)}</td><td>{escape(p.status)}</td></tr>"
        for p in projects
    )
    asset_rows = "\n".join(
        f"<tr><td>{escape(a.path)}</td><td>{escape(a.kind)}</td><td>{escape(a.project_slug)}</td></tr>"
        for a in assets
    )
    return f"""<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>ZAI Creative Automation</title>
  <style>
    body {{ font-family: system-ui, sans-serif; margin: 2rem; background: #0f172a; color: #e2e8f0; }}
    table {{ border-collapse: collapse; width: 100%; margin: 1rem 0; }}
    th, td {{ border: 1px solid #334155; padding: 0.6rem; text-align: left; }}
    th {{ background: #1e293b; }}
    .card {{ border: 1px solid #334155; border-radius: 12px; padding: 1rem; margin-bottom: 1rem; }}
  </style>
</head>
<body>
  <h1>ZAI Creative Automation</h1>
  <div class="card">
    <h2>Projects</h2>
    <table><thead><tr><th>Slug</th><th>Title</th><th>Type</th><th>Status</th></tr></thead><tbody>{project_rows}</tbody></table>
  </div>
  <div class="card">
    <h2>Assets</h2>
    <table><thead><tr><th>Path</th><th>Kind</th><th>Project</th></tr></thead><tbody>{asset_rows}</tbody></table>
  </div>
</body>
</html>
"""
