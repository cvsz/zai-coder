"""Usage analytics reports and exports."""

from __future__ import annotations

import json
import uuid
from pathlib import Path

from .aggregator import metric_snapshots, aggregate_usage
from .insights import generate_insights
from .models import AnalyticsReport
from .privacy import export_safety_gate, analytics_retention_policy


def build_analytics_report(events: list[dict], period: str = "current") -> AnalyticsReport:
    report = AnalyticsReport(
        id=f"uar_{uuid.uuid4().hex[:12]}",
        title="Usage Analytics and Insights Report",
        period=period,
        metrics=tuple(metric_snapshots(events, period)),
        insights=tuple(generate_insights(events)),
    )
    issues = report.validate()
    if issues:
        raise ValueError("; ".join(issues))
    return report


def analytics_report_markdown(report: AnalyticsReport | dict) -> str:
    payload = report.to_dict() if hasattr(report, "to_dict") else report
    metrics = "\n".join(f"- {m['metric']}: {m['value']} {m['unit']}" for m in payload["metrics"])
    insights = "\n".join(f"- [{i['severity']}] {i['title']}: {i['summary']}" for i in payload["insights"]) or "- No insights generated."
    return f"""# {payload['title']}

Period: {payload['period']}

## Metrics

{metrics}

## Insights

{insights}

## Privacy and Safety

- Local analytics only.
- Raw PII is not allowed in usage metadata.
- Exports are reviewable and dry-run by default.
"""


def export_analytics_report(report: AnalyticsReport, root: str | Path = ".", out_dir: str = "analytics/reports") -> dict:
    root = Path(root)
    out = root / out_dir
    out.mkdir(parents=True, exist_ok=True)
    json_path = out / f"{report.id}.json"
    md_path = out / f"{report.id}.md"
    json_path.write_text(json.dumps(report.to_dict(), indent=2, sort_keys=True), encoding="utf-8")
    md_path.write_text(analytics_report_markdown(report), encoding="utf-8")
    return {"json": str(json_path), "markdown": str(md_path), "safety": export_safety_gate(report.to_dict())}


def analytics_export_bundle(events: list[dict]) -> dict:
    report = build_analytics_report(events)
    return {
        "kind": "zai-usage-analytics-export",
        "version": "1.0",
        "aggregate": aggregate_usage(events),
        "report": report.to_dict(),
        "retention": analytics_retention_policy(),
        "raw_events_included": False,
        "external_publish": False,
    }


def write_analytics_export(events: list[dict], root: str | Path = ".", out: str = "analytics/exports/usage-analytics-export.json") -> str:
    root = Path(root)
    path = root / out
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(analytics_export_bundle(events), indent=2, sort_keys=True), encoding="utf-8")
    return str(path)
