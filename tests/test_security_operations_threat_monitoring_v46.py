from pathlib import Path
from zai_coder.security_operations_threat_monitoring.models import ThreatSignal, PolicyAlert, IncidentPlan, SecurityEvidence
from zai_coder.security_operations_threat_monitoring.core import *
from zai_coder.security_operations_threat_monitoring.routes import *

def test_models_validation():
    assert ThreatSignal("s","Signal","auth_anomaly","local").validate() == []
    assert ThreatSignal("","","bad","secret token", severity="bad", status="bad").validate()
    assert PolicyAlert("a","policy","Alert").validate() == []
    assert PolicyAlert("","","", severity="bad", action="bad", status="bad").validate()
    assert IncidentPlan("i","Incident","access_review").validate() == []
    assert IncidentPlan("","","bad", severity="bad", status="bad", dry_run=False).validate()
    assert SecurityEvidence("e","signal_summary","Evidence").validate() == []
    assert SecurityEvidence("","","", redacted=False, status="bad").validate()

def test_core_security_ops():
    assert threat_signal_registry()
    assert policy_alert_catalog()
    assert incident_workflow_plans()
    assert security_evidence_catalog()
    assert validation_report()["ok"]
    assert risk_scorecard()["dry_run"]
    assert alert_review_queue()["auto_blocking"] is False
    assert incident_workflow_plan()["execute_response"] is False
    bundle = security_evidence_bundle()
    assert bundle["active_blocking"] is False
    assert bundle["requires_review"] is True

def test_exports(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert Path(write_security_evidence(tmp_path)).exists()
    assert Path(write_security_report(tmp_path)).exists()
    demo = security_ops_demo(str(tmp_path))
    assert Path(demo["evidence_path"]).exists()
    assert Path(demo["report_path"]).exists()

def test_routes():
    assert route_security_ops_status()["ok"]
    assert route_security_ops_overview()["validation"]["ok"]
    assert route_threat_signals()["signals"]
    assert route_policy_alerts()["queue"]["requires_human_review"]
    assert route_incident_workflow_plan()["execute_response"] is False
    assert "evidence_path" in route_security_evidence_export()
    assert "evidence_path" in route_security_ops_demo()
    assert route_security_ops_page()["content_type"] == "text/html"
    assert route_security_signals_page()["content_type"] == "text/html"
    assert route_security_alerts_page()["content_type"] == "text/html"
    assert route_security_incidents_page()["content_type"] == "text/html"
    assert route_security_evidence_page()["content_type"] == "text/html"

def test_docs_scripts_assets_exist():
    root = Path(__file__).resolve().parents[1]
    for rel in [
        "scripts/security-ops/security-ops-status.sh",
        "scripts/security-ops/threat-signals.sh",
        "scripts/security-ops/policy-alerts.sh",
        "scripts/security-ops/incident-workflow-plan.sh",
        "scripts/security-ops/security-evidence-export.sh",
        "scripts/security-ops/security-ops-demo.sh",
        "scripts/security-ops/security-dashboard-export.sh",
        "docs/security-ops/SECURITY_OPERATIONS_THREAT_MONITORING_GUIDE.md",
        "docs/security-ops/THREAT_SIGNAL_REGISTRY.md",
        "docs/security-ops/POLICY_ALERTS.md",
        "docs/security-ops/INCIDENT_WORKFLOW_POLICY.md",
        "docs/security-ops/SECURITY_EVIDENCE_POLICY.md",
        "docs/requirements/NEXT_V46_SECURITY_OPERATIONS_THREAT_MONITORING_REQUIREMENTS.md",
        "assets/security-ops/security_operations_threat_monitoring_features.json",
    ]:
        assert (root / rel).exists(), rel
