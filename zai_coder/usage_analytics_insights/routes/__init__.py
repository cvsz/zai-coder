"""Usage Analytics and Insights route registry."""

from __future__ import annotations

from zai_coder.usage_analytics_insights.control import usage_analytics_status, analytics_overview, analytics_demo
from zai_coder.usage_analytics_insights.events import UsageEventLedger, seed_demo_events
from zai_coder.usage_analytics_insights.aggregator import aggregate_usage, metric_snapshots, customer_breakdown
from zai_coder.usage_analytics_insights.funnels import adoption_funnel, activation_score
from zai_coder.usage_analytics_insights.anomaly import detect_usage_anomalies, anomaly_policy
from zai_coder.usage_analytics_insights.insights import generate_insights
from zai_coder.usage_analytics_insights.reporting import build_analytics_report, analytics_report_markdown, write_analytics_export
from zai_coder.usage_analytics_insights.privacy import analytics_retention_policy, privacy_gate, export_safety_gate
from zai_coder.usage_analytics_insights.audit import AnalyticsAuditLog
from zai_coder.usage_analytics_insights.ui.pages import render_analytics_overview_page, render_metrics_page, render_insights_page, render_funnel_page, render_privacy_page


def route_usage_analytics_status() -> dict:
    return {
        "ok": True,
        "service": "zai-usage-analytics-and-insights",
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


def route_analytics_overview() -> dict:
    return analytics_overview()


def route_analytics_seed_demo() -> dict:
    return {"events": seed_demo_events()}


def route_analytics_metrics() -> dict:
    events = seed_demo_events("data/usage-analytics-routes.db")
    return {"aggregate": aggregate_usage(events), "metrics": metric_snapshots(events), "customer_breakdown": customer_breakdown(events)}


def route_analytics_funnel() -> dict:
    events = seed_demo_events("data/usage-analytics-funnel.db")
    return {"funnel": adoption_funnel(events), "activation": activation_score(events, "cust_demo")}


def route_analytics_insights() -> dict:
    events = seed_demo_events("data/usage-analytics-insights.db")
    return {"insights": generate_insights(events), "anomalies": detect_usage_anomalies(aggregate_usage(events)), "policy": anomaly_policy()}


def route_analytics_report_demo() -> dict:
    return analytics_demo("data/usage-analytics-report.db", ".")


def route_analytics_report_markdown() -> dict:
    events = seed_demo_events("data/usage-analytics-md.db")
    report = build_analytics_report(events, "demo")
    return {"markdown": analytics_report_markdown(report), "report": report.to_dict()}


def route_analytics_privacy() -> dict:
    report = {"id": "demo", "dry_run": True}
    return {"retention": analytics_retention_policy(), "privacy_gate": privacy_gate({"metadata": {"source": "demo"}}), "export_gate": export_safety_gate(report)}


def route_analytics_export() -> dict:
    events = seed_demo_events("data/usage-analytics-export.db")
    return {"path": write_analytics_export(events, ".")}


def route_analytics_audit() -> dict:
    return {"events": AnalyticsAuditLog().list_events()}


def route_analytics_page() -> dict:
    return {"content_type": "text/html", "html": render_analytics_overview_page()}


def route_analytics_metrics_page() -> dict:
    return {"content_type": "text/html", "html": render_metrics_page()}


def route_analytics_insights_page() -> dict:
    return {"content_type": "text/html", "html": render_insights_page()}


def route_analytics_funnel_page() -> dict:
    return {"content_type": "text/html", "html": render_funnel_page()}


def route_analytics_privacy_page() -> dict:
    return {"content_type": "text/html", "html": render_privacy_page()}
