"""Rendered content export helpers."""

from __future__ import annotations

import json
from pathlib import Path

from .render import render_demo_content
from .library import content_library_bundle


def write_rendered_content(rendered: dict, root: str | Path = ".", out_dir: str = "content/rendered") -> dict:
    root = Path(root)
    out = root / out_dir
    out.mkdir(parents=True, exist_ok=True)
    json_path = out / f"{rendered['id']}.json"
    md_path = out / f"{rendered['id']}.md"
    json_path.write_text(json.dumps(rendered, indent=2, sort_keys=True), encoding="utf-8")
    md_path.write_text(rendered["content"], encoding="utf-8")
    return {"json": str(json_path), "markdown": str(md_path)}


def content_studio_export_bundle() -> dict:
    demo = render_demo_content()
    return {
        "kind": "zai-template-content-studio-export",
        "version": "1.0",
        "library": content_library_bundle("customer"),
        "demo_rendered": demo["rendered"],
        "safety": demo["safety"],
        "external_publish": False,
        "requires_review": True,
    }


def write_content_studio_export(root: str | Path = ".", out: str = "content/exports/template-content-studio-export.json") -> str:
    root = Path(root)
    path = root / out
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(content_studio_export_bundle(), indent=2, sort_keys=True), encoding="utf-8")
    return str(path)


def write_content_report(root: str | Path = ".", out: str = "content/reports/template-content-studio-report.md") -> str:
    bundle = content_studio_export_bundle()
    root = Path(root)
    path = root / out
    path.parent.mkdir(parents=True, exist_ok=True)
    templates = "\n".join(f"- {item['title']} [{item['template_type']} / {item['visibility']}]" for item in bundle["library"]["templates"])
    path.write_text(f"""# Template and Content Studio Report

## Templates

{templates}

## Demo Render

```text
{bundle['demo_rendered']['content']}
```

## Safety

- Local render only.
- External publishing is disabled.
- Human review is required before external use.
""", encoding="utf-8")
    return str(path)
