from pathlib import Path

from zai_coder.observability_suite.models import MetricSample, StructuredEvent, AlertRule
from zai_coder.observability_suite.metrics import MetricsRegistry, render_prometheus_metrics, default_metrics_registry
from zai_coder.observability_suite.event_bus import StructuredEventBus, default_event_bus
from zai_coder.observability_suite.alerts import evaluate_alerts, alert_rules_manifest
from zai_coder.observability_suite.health_trends import HealthSnapshot, HealthTrendStore, default_health_trend_store
from zai_coder.observability_suite.dashboards import render_observability_overview, render_metrics_dashboard, render_alerts_dashboard, render_health_trends_dashboard
from zai_coder.observability_suite.log_retention import default_log_retention_policy
from zai_coder.observability_suite.incident_report import incident_report_template
from zai_coder.observability_suite.slo_sla import slo_templates, sla_template
from zai_coder.observability_suite.uptime import uptime_verification_plan
from zai_coder.observability_suite.routes import (
    route_observability_status,
    route_metrics_json,
    route_metrics_prometheus,
    route_alert_rules,
    route_alerts_evaluate,
    route_health_trends,
    route_log_retention,
    route_incident_template,
    route_slo_templates,
    route_uptime_plan,
    route_observability_page,
    route_metrics_page,
    route_alerts_page,
    route_health_trends_page,
)


def test_models_validate_and_alert_evaluate():
    assert MetricSample("metric", 1).validate() == []
    assert MetricSample("", 1).validate()
    assert StructuredEvent("topic", "info", "msg").validate() == []
    assert StructuredEvent("", "bad", "").validate()
    rule = AlertRule("high", "m", ">", 10)
    assert rule.evaluate(11) is True
    assert rule.evaluate(9) is False


def test_metrics_registry_and_prometheus():
    registry = MetricsRegistry()
    registry.gauge("zai_health_ok", 1, {"service": "api"})
    registry.increment("zai_requests_total", 2)
    registry.increment("zai_requests_total", 3)
    samples = registry.samples()
    assert len(samples) == 2
    prom = render_prometheus_metrics(samples)
    assert "zai_health_ok" in prom
    assert "zai_requests_total 5" in prom
    assert default_metrics_registry().samples()


def test_event_bus():
    bus = StructuredEventBus()
    seen = []
    bus.subscribe("*", lambda event: seen.append(event.topic))
    bus.publish(StructuredEvent("system.test", "info", "hello"))
    assert seen == ["system.test"]
    assert bus.list_events()[0]["topic"] == "system.test"
    assert default_event_bus().list_events()


def test_alerts_and_health_trends():
    samples = [MetricSample("zai_health_ok", 0), MetricSample("zai_queue_depth", 101)]
    alerts = evaluate_alerts(samples)
    assert alerts
    assert alert_rules_manifest()
    store = HealthTrendStore()
    snap = HealthSnapshot("ok", 5, 4, 10)
    store.add(snap)
    assert store.summary()["snapshots"] == 1
    assert store.list_snapshots()[0]["ok_ratio"] == 0.8
    assert default_health_trend_store().summary()["ok"] is True


def test_dashboards_and_policies():
    assert "Observability Suite" in render_observability_overview()
    assert "Metrics" in render_metrics_dashboard([MetricSample("m", 1).to_dict()])
    assert "Alerts" in render_alerts_dashboard([])
    assert "Health Trends" in render_health_trends_dashboard([HealthSnapshot("ok", 1, 1).to_dict()])
    policy = default_log_retention_policy()
    assert policy.validate() == []
    assert "apps/zlms/" in policy.exclude_paths


def test_incident_slo_uptime():
    report = incident_report_template()
    assert report.validate() == []
    md = report.to_markdown()
    assert "Incident Report" in md
    assert slo_templates()
    assert sla_template()["response_targets"]["sev1"]
    plan = uptime_verification_plan()
    assert plan["dry_run"] is True
    assert any("/healthz" in c for c in plan["local_checks"])


def test_routes():
    assert route_observability_status()["ok"] is True
    assert route_metrics_json()["samples"]
    assert route_metrics_prometheus()["content_type"] == "text/plain"
    assert "zai_health_ok" in route_metrics_prometheus()["text"]
    assert route_alert_rules()["rules"]
    assert "alerts" in route_alerts_evaluate()
    assert route_health_trends()["summary"]["ok"] is True
    assert route_log_retention()["issues"] == []
    assert route_incident_template()["content_type"] == "text/markdown"
    assert route_slo_templates()["slos"]
    assert route_uptime_plan()["dry_run"] is True
    assert route_observability_page()["content_type"] == "text/html"
    assert route_metrics_page()["content_type"] == "text/html"
    assert route_alerts_page()["content_type"] == "text/html"
    assert route_health_trends_page()["content_type"] == "text/html"


def test_docs_scripts_assets_exist():
    root = Path(__file__).resolve().parents[1]
    for rel in [
        "scripts/observability/observability-status.sh",
        "scripts/observability/metrics-export.sh",
        "scripts/observability/alerts-evaluate.sh",
        "scripts/observability/health-trends.sh",
        "scripts/observability/log-retention-policy.sh",
        "scripts/observability/incident-template.sh",
        "scripts/observability/slo-sla-templates.sh",
        "scripts/observability/uptime-plan.sh",
        "scripts/observability/dashboard-export.sh",
        "docs/observability/OBSERVABILITY_SUITE_GUIDE.md",
        "docs/observability/METRICS_AND_ALERTS.md",
        "docs/observability/INCIDENT_REPORTING.md",
        "docs/observability/SLO_SLA_TEMPLATES.md",
        "docs/observability/UPTIME_VERIFICATION.md",
        "docs/requirements/NEXT_V19_OBSERVABILITY_SUITE_REQUIREMENTS.md",
        "assets/observability/observability_suite_features.json",
    ]:
        assert (root / rel).exists(), rel
