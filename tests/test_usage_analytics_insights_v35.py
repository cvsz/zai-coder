from pathlib import Path

from zai_coder.usage_analytics_insights.models import UsageEvent, MetricSnapshot, Insight, AnalyticsReport
from zai_coder.usage_analytics_insights.privacy import redact_metadata, privacy_gate, analytics_retention_policy, export_safety_gate
from zai_coder.usage_analytics_insights.events import UsageEventLedger, seed_demo_events
from zai_coder.usage_analytics_insights.aggregator import aggregate_usage, metric_snapshots, customer_breakdown
from zai_coder.usage_analytics_insights.funnels import adoption_funnel, activation_score
from zai_coder.usage_analytics_insights.anomaly import detect_usage_anomalies, anomaly_policy
from zai_coder.usage_analytics_insights.insights import generate_insights
from zai_coder.usage_analytics_insights.reporting import build_analytics_report, analytics_report_markdown, export_analytics_report, analytics_export_bundle, write_analytics_export
from zai_coder.usage_analytics_insights.audit import AnalyticsAuditLog
from zai_coder.usage_analytics_insights.control import usage_analytics_status, analytics_demo, analytics_overview
from zai_coder.usage_analytics_insights.ui.pages import render_analytics_overview_page, render_metrics_page, render_insights_page, render_funnel_page, render_privacy_page
from zai_coder.usage_analytics_insights.routes import (
    route_usage_analytics_status,
    route_analytics_overview,
    route_analytics_seed_demo,
    route_analytics_metrics,
    route_analytics_funnel,
    route_analytics_insights,
    route_analytics_report_demo,
    route_analytics_report_markdown,
    route_analytics_privacy,
    route_analytics_export,
    route_analytics_audit,
    route_analytics_page,
    route_analytics_metrics_page,
    route_analytics_insights_page,
    route_analytics_funnel_page,
    route_analytics_privacy_page,
)


def test_models_and_privacy():
    assert UsageEvent("e", "feature.use", "c", "o", "w").validate() == []
    assert UsageEvent("", "", "", "", "", quantity=-1, metadata={"email": "x"}).validate()
    assert MetricSnapshot("m", "total_events", 1, "today").validate() == []
    assert Insight("i", "Title", "info", "usage", "Summary").validate() == []
    assert AnalyticsReport("r", "Report", "today", ({"metric":"x","value":1},), ()).validate() == []
    assert redact_metadata({"token": "secret", "source": "demo"})["token"] == "<redacted>"
    assert privacy_gate({"metadata": {"source": "demo"}})["allowed"] is True
    assert privacy_gate({"metadata": {"email": "x@example.local"}})["allowed"] is False
    assert analytics_retention_policy()["no_pii_by_default"] is True
    assert export_safety_gate({"id": "r", "dry_run": True})["allowed"] is True
    assert export_safety_gate({"id": "r", "dry_run": True}, external_publish_requested=True)["allowed"] is False


def test_ledger_aggregation_funnel_insights(tmp_path):
    ledger = UsageEventLedger(tmp_path / "usage.db")
    event = ledger.record_event("feature.use", "cust", "org", "ws", "actor", "dashboard", 2, {"source": "test"})
    assert event.id.startswith("ue_")
    assert ledger.list_events("cust")[0]["feature_id"] == "dashboard"
    try:
        ledger.record_event("feature.use", "cust", "org", "ws", metadata={"token": "x"})
        assert False
    except ValueError:
        assert True
    events = seed_demo_events(tmp_path / "usage2.db")
    agg = aggregate_usage(events, "demo")
    assert agg["total_events"] == 5
    assert metric_snapshots(events, "demo")
    assert customer_breakdown(events)["cust_demo"]["total_events"] == 4
    funnel = adoption_funnel(events)
    assert funnel["counts"]["portal.view"] >= 1
    activation = activation_score(events, "cust_demo")
    assert activation["score"] > 0
    anomalies = detect_usage_anomalies(agg)
    assert "anomalies" in anomalies
    assert anomaly_policy()["no_external_ml_call"] is True
    assert generate_insights(events)


def test_reporting_audit_control(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    events = seed_demo_events(tmp_path / "usage.db")
    report = build_analytics_report(events, "demo")
    assert report.dry_run is True
    assert "Usage Analytics" in analytics_report_markdown(report)
    exports = export_analytics_report(report, tmp_path)
    assert Path(exports["json"]).exists()
    assert Path(exports["markdown"]).exists()
    bundle = analytics_export_bundle(events)
    assert bundle["raw_events_included"] is False
    export_path = write_analytics_export(events, tmp_path)
    assert Path(export_path).exists()
    audit = AnalyticsAuditLog(tmp_path / "analytics.db")
    audit_event = audit.record("tester", "analytics.test", report.id)
    assert audit.list_events()[0]["id"] == audit_event.id
    assert usage_analytics_status()["ok"] is True
    demo = analytics_demo(str(tmp_path / "demo.db"), str(tmp_path))
    assert demo["events_recorded"] == 5
    assert Path(demo["export_path"]).exists()
    overview = analytics_overview()
    assert overview["status"]["ok"] is True


def test_ui_routes(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert "Usage Analytics and Insights" in render_analytics_overview_page()
    assert "Metrics" in render_metrics_page()
    assert "Insights" in render_insights_page()
    assert "Funnel" in render_funnel_page()
    assert "Privacy" in render_privacy_page()
    assert route_usage_analytics_status()["ok"] is True
    assert route_analytics_overview()["status"]["ok"] is True
    assert route_analytics_seed_demo()["events"]
    assert route_analytics_metrics()["aggregate"]["total_events"] == 5
    assert route_analytics_funnel()["activation"]["customer_id"] == "cust_demo"
    assert route_analytics_insights()["insights"]
    assert Path(route_analytics_report_demo()["export_path"]).exists()
    assert "markdown" in route_analytics_report_markdown()
    assert route_analytics_privacy()["retention"]["no_pii_by_default"] is True
    assert Path(route_analytics_export()["path"]).exists()
    assert "events" in route_analytics_audit()
    assert route_analytics_page()["content_type"] == "text/html"
    assert route_analytics_metrics_page()["content_type"] == "text/html"
    assert route_analytics_insights_page()["content_type"] == "text/html"
    assert route_analytics_funnel_page()["content_type"] == "text/html"
    assert route_analytics_privacy_page()["content_type"] == "text/html"


def test_docs_scripts_assets_exist():
    root = Path(__file__).resolve().parents[1]
    for rel in [
        "scripts/usage-analytics/analytics-status.sh",
        "scripts/usage-analytics/analytics-seed-demo.sh",
        "scripts/usage-analytics/analytics-metrics.sh",
        "scripts/usage-analytics/analytics-funnel.sh",
        "scripts/usage-analytics/analytics-insights.sh",
        "scripts/usage-analytics/analytics-report-demo.sh",
        "scripts/usage-analytics/analytics-report-markdown.sh",
        "scripts/usage-analytics/analytics-privacy.sh",
        "scripts/usage-analytics/analytics-export.sh",
        "scripts/usage-analytics/analytics-audit.sh",
        "scripts/usage-analytics/analytics-dashboard-export.sh",
        "docs/usage-analytics/USAGE_ANALYTICS_INSIGHTS_GUIDE.md",
        "docs/usage-analytics/USAGE_EVENT_LEDGER.md",
        "docs/usage-analytics/PRIVACY_RETENTION.md",
        "docs/usage-analytics/ADOPTION_FUNNEL.md",
        "docs/usage-analytics/ANOMALY_INSIGHTS.md",
        "docs/usage-analytics/ANALYTICS_EXPORT_POLICY.md",
        "docs/requirements/NEXT_V35_USAGE_ANALYTICS_INSIGHTS_REQUIREMENTS.md",
        "assets/usage-analytics/usage_analytics_insights_features.json",
    ]:
        assert (root / rel).exists(), rel
