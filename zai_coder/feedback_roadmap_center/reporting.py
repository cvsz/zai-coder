"""Feedback and roadmap reports."""

from __future__ import annotations

import json
from pathlib import Path

from .feedback import feedback_triage
from .roadmap import roadmap_registry, roadmap_by_visibility
from .prioritization import prioritization_matrix
from .linker import link_feedback_to_roadmap
from .changelog_loop import changelog_feedback_summary


def roadmap_report_payload(feedback_items: list[dict]) -> dict:
    roadmap = roadmap_registry()
    return {
        "kind": "zai-feedback-roadmap-report",
        "version": "1.0",
        "feedback_triage": [feedback_triage(item) for item in feedback_items],
        "feedback_summary": changelog_feedback_summary(feedback_items),
        "roadmap": roadmap,
        "customer_view": roadmap_by_visibility("customer"),
        "prioritization": prioritization_matrix(roadmap),
        "links": link_feedback_to_roadmap(feedback_items, roadmap),
        "external_publish": False,
        "requires_review": True,
    }


def roadmap_report_markdown(feedback_items: list[dict]) -> str:
    payload = roadmap_report_payload(feedback_items)
    roadmap = "\n".join(f"- {item['title']} [{item['horizon']} / {item['status']} / {item['visibility']}]" for item in payload["roadmap"])
    triage = "\n".join(f"- {item['feedback_id']}: {item['queue']} score={item['score']}" for item in payload["feedback_triage"])
    return f"""# Feedback and Roadmap Center Report

## Feedback Triage

{triage}

## Roadmap

{roadmap}

## Feedback Summary

```json
{json.dumps(payload['feedback_summary'], indent=2, sort_keys=True)}
```

## Safety

- Report is local/export-only.
- Public roadmap publishing is disabled.
- Customer-visible views exclude private roadmap items.
"""


def write_roadmap_report(feedback_items: list[dict], root: str | Path = ".", out_dir: str = "roadmap/reports") -> dict:
    root = Path(root)
    out = root / out_dir
    out.mkdir(parents=True, exist_ok=True)
    payload = roadmap_report_payload(feedback_items)
    json_path = out / "feedback-roadmap-report.json"
    md_path = out / "feedback-roadmap-report.md"
    json_path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    md_path.write_text(roadmap_report_markdown(feedback_items), encoding="utf-8")
    return {"json": str(json_path), "markdown": str(md_path)}
