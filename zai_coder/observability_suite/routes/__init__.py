"""Observability suite route registry."""

from __future__ import annotations

from zai_coder.observability_suite.metrics import default_metrics_registry, render_prometheus_metrics
from zai_coder.observability_suite.alerts import evaluate_alerts, alert_rules_manifest
from zai_coder.observability_suite.health_trends import default_health_trend_store
from zai_coder.observability_suite.log_retention import default_log_retention_policy
from zai_coder.observability_suite.incident_report import incident_report_template
from zai_coder.observability_suite.slo_sla import slo_templates, sla_template
from zai_coder.observability_suite.uptime import uptime_verification_plan
from zai_coder.observability_suite.dashboards import (
    render_observability_overview,
    render_metrics_dashboard,
    render_alerts_dashboard,
    render_health_trends_dashboard,
)


def route_observability_status() -> dict:
    return {
        "ok": True,
        "service": "zai-observability-suite",
        "systems": [
            "metrics_registry",
            "prometheus_metrics_endpoint",
            "structured_event_bus",
            "alert_rules",
            "health_trend_snapshots",
            "execution_provider_dashboards",
            "log_retention_policy",
            "incident_report_generator",
            "slo_sla_templates",
            "uptime_verification_plan",
        ],
    }


def route_metrics_json() -> dict:
    registry = default_metrics_registry()
    return {"samples": [sample.to_dict() for sample in registry.samples()]}


def route_metrics_prometheus() -> dict:
    registry = default_metrics_registry()
    return {"content_type": "text/plain", "text": render_prometheus_metrics(registry.samples())}


def route_alert_rules() -> dict:
    return {"rules": alert_rules_manifest()}


def route_alerts_evaluate() -> dict:
    registry = default_metrics_registry()
    return {"alerts": evaluate_alerts(registry.samples())}


def route_health_trends() -> dict:
    store = default_health_trend_store()
    return {"summary": store.summary(), "snapshots": store.list_snapshots()}


def route_log_retention() -> dict:
    policy = default_log_retention_policy()
    return {"policy": policy.to_dict(), "issues": policy.validate()}


def route_incident_template(title: str = "Service degradation", severity: str = "sev3") -> dict:
    report = incident_report_template(title, severity)
    return {"content_type": "text/markdown", "markdown": report.to_markdown(), "issues": report.validate()}


def route_slo_templates() -> dict:
    return {"slos": slo_templates(), "sla": sla_template()}


def route_uptime_plan(base_url: str = "http://127.0.0.1:8765", public_url: str = "https://zai.example.com") -> dict:
    return uptime_verification_plan(base_url, public_url)


def route_observability_page() -> dict:
    return {"content_type": "text/html", "html": render_observability_overview()}


def route_metrics_page() -> dict:
    return {"content_type": "text/html", "html": render_metrics_dashboard(route_metrics_json()["samples"])}


def route_alerts_page() -> dict:
    return {"content_type": "text/html", "html": render_alerts_dashboard(route_alerts_evaluate()["alerts"])}


def route_health_trends_page() -> dict:
    return {"content_type": "text/html", "html": render_health_trends_dashboard(route_health_trends()["snapshots"])}
