"""Content library and exports."""

from __future__ import annotations

import json
from pathlib import Path

from .templates import template_registry, template_validation_report, templates_by_visibility
from .faq_bridge import help_article_template_map
from .brand import brand_rules


def content_library_bundle(visibility: str = "customer") -> dict:
    return {
        "kind": "zai-template-content-library",
        "version": "1.0",
        "visibility": visibility,
        "templates": templates_by_visibility(visibility),
        "template_validation": template_validation_report(),
        "help_article_map": help_article_template_map(),
        "brand_rules": brand_rules(),
        "external_publish": False,
        "requires_review": True,
    }


def write_content_library_export(root: str | Path = ".", visibility: str = "customer", out: str = "content/exports/content-library-export.json") -> str:
    root = Path(root)
    path = root / out
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(content_library_bundle(visibility), indent=2, sort_keys=True), encoding="utf-8")
    return str(path)
