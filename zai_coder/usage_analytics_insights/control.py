"""Usage analytics and insights control helpers."""

from __future__ import annotations

from .events import UsageEventLedger, seed_demo_events
from .aggregator import aggregate_usage, metric_snapshots, customer_breakdown
from .funnels import adoption_funnel
from .anomaly import detect_usage_anomalies, anomaly_policy
from .insights import generate_insights
from .reporting import build_analytics_report, export_analytics_report, write_analytics_export
from .privacy import analytics_retention_policy, privacy_gate
from .audit import AnalyticsAuditLog


def usage_analytics_status() -> dict:
    return {
        "ok": True,
        "systems": [
            "usage_event_ledger",
            "metric_aggregation",
            "customer_workspace_breakdown",
            "adoption_funnel",
            "activation_scoring",
            "anomaly_detection",
            "insight_generator",
            "privacy_retention_guard",
            "analytics_report_exports",
            "analytics_audit_log",
        ],
    }


def analytics_demo(db_path: str = "data/usage-analytics.db", root: str = ".") -> dict:
    events = seed_demo_events(db_path)
    report = build_analytics_report(events, "demo")
    exports = export_analytics_report(report, root)
    export_path = write_analytics_export(events, root)
    audit = AnalyticsAuditLog(db_path).record("system", "analytics.report_generated", report.id, {"export_path": export_path})
    return {
        "events_recorded": len(events),
        "aggregate": aggregate_usage(events, "demo"),
        "metrics": metric_snapshots(events, "demo"),
        "customer_breakdown": customer_breakdown(events),
        "funnel": adoption_funnel(events),
        "anomalies": detect_usage_anomalies(aggregate_usage(events)),
        "insights": generate_insights(events),
        "report": report.to_dict(),
        "exports": exports,
        "export_path": export_path,
        "audit": audit.to_dict(),
    }


def analytics_overview() -> dict:
    events = seed_demo_events("data/usage-analytics-overview.db")
    return {
        "status": usage_analytics_status(),
        "aggregate": aggregate_usage(events),
        "funnel": adoption_funnel(events),
        "insights": generate_insights(events),
        "retention": analytics_retention_policy(),
        "anomaly_policy": anomaly_policy(),
        "privacy_gate_demo": privacy_gate({"metadata": {"source": "demo"}}),
    }
