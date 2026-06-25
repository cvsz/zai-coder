"""Help center exports."""

from __future__ import annotations

import json
from pathlib import Path

from .articles import article_by_visibility, article_validation_report
from .faq import faq_catalog, faq_validation_report
from .deflection import deflection_policy


def help_export_bundle(visibility: str = "customer") -> dict:
    return {
        "kind": "zai-help-center-export",
        "version": "1.0",
        "visibility": visibility,
        "articles": article_by_visibility(visibility),
        "faqs": [item for item in faq_catalog() if visibility == "private" or item["visibility"] in {"customer", "public"}],
        "article_validation": article_validation_report(),
        "faq_validation": faq_validation_report(),
        "deflection_policy": deflection_policy(),
        "external_publish": False,
        "requires_review": True,
    }


def write_help_export(root: str | Path = ".", visibility: str = "customer", out: str = "help/exports/help-center-export.json") -> str:
    root = Path(root)
    path = root / out
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(help_export_bundle(visibility), indent=2, sort_keys=True), encoding="utf-8")
    return str(path)


def help_report_markdown(visibility: str = "customer") -> str:
    bundle = help_export_bundle(visibility)
    articles = "\n".join(f"- {item['title']} [{item['category']} / {item['visibility']}]" for item in bundle["articles"])
    faqs = "\n".join(f"- {item['question']}" for item in bundle["faqs"])
    return f"""# Knowledge Base and Help Center Report

## Articles

{articles}

## FAQs

{faqs}

## Safety

- Local export only.
- External publishing is disabled.
- Customer views exclude private/internal articles.
- Human review required before publishing.
"""


def write_help_report(root: str | Path = ".", visibility: str = "customer", out: str = "help/reports/help-center-report.md") -> str:
    root = Path(root)
    path = root / out
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(help_report_markdown(visibility), encoding="utf-8")
    return str(path)
