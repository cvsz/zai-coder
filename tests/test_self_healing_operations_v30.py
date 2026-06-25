from pathlib import Path
import tempfile

from zai_coder.self_healing_operations.models import HealthSignal, Incident, RemediationPlaybook, HealingPlan
from zai_coder.self_healing_operations.signals import classify_signal, create_signal, signal_summary
from zai_coder.self_healing_operations.detector import detect_incident, severity_from_signals, incident_triage_plan
from zai_coder.self_healing_operations.playbooks import playbook_catalog, find_playbook, match_playbook, validate_playbook_catalog
from zai_coder.self_healing_operations.guardrails import maintenance_window_policy, action_guard, auto_heal_gate, rollback_guard
from zai_coder.self_healing_operations.planner import build_healing_plan, write_healing_plan, healing_readiness
from zai_coder.self_healing_operations.escalation import escalation_policy, escalation_decision, notification_draft
from zai_coder.self_healing_operations.postmortem import postmortem_markdown, write_postmortem
from zai_coder.self_healing_operations.audit import HealingAuditLog
from zai_coder.self_healing_operations.control import self_healing_status, demo_signals, incident_demo, healing_plan_demo, self_healing_overview
from zai_coder.self_healing_operations.ui.pages import render_healing_overview, render_incidents_page, render_playbooks_page, render_policy_page
from zai_coder.self_healing_operations.routes import (
    route_self_healing_status,
    route_self_healing_overview,
    route_signal_demo,
    route_incident_demo,
    route_playbook_catalog,
    route_guardrail_policy,
    route_healing_plan_demo,
    route_escalation_demo,
    route_postmortem_demo,
    route_healing_audit,
    route_self_healing_page,
    route_self_healing_incidents_page,
    route_self_healing_playbooks_page,
    route_self_healing_policy_page,
)


def test_models_validation():
    assert HealthSignal("s", "src", "error_rate", 0.01).validate() == []
    assert HealthSignal("", "", "", -1, status="bad").validate()
    assert Incident("i", "Title", "high", "core").validate() == []
    assert Incident("", "", "bad", "", status="bad").validate()
    assert RemediationPlaybook("p", "Playbook", "core", "error_rate", ("make healthcheck",)).validate() == []
    assert RemediationPlaybook("", "", "", "", ("rm -rf /",), risk_level="bad").validate()
    assert HealingPlan("h", "i", "p", ("make healthcheck",), rollback_plan=("rollback",)).validate() == []


def test_signals_detector_playbooks():
    assert classify_signal("error_rate", 0.06) == "critical"
    assert classify_signal("queue_depth", 250) == "warning"
    signals = [create_signal("gateway", "error_rate", 0.06), create_signal("workers", "queue_depth", 250)]
    summary = signal_summary(signals)
    assert summary["worst"] == "critical"
    assert severity_from_signals(signals) == "high"
    detected = detect_incident(signals, "core")
    assert detected["detected"] is True
    triage = incident_triage_plan(detected["incident"])
    assert triage["dry_run"] is True
    assert playbook_catalog()
    assert find_playbook("restart-local-service").service == "core"
    assert match_playbook("core", "heartbeat_age_seconds").id == "restart-local-service"
    assert validate_playbook_catalog()["ok"] is True


def test_guardrails_and_planner(tmp_path):
    assert maintenance_window_policy()["approval_required_outside_window"] is True
    assert action_guard(["make healthcheck"])["allowed"] is True
    assert action_guard(["rm -rf /"])["allowed"] is False
    playbook = find_playbook("rollback-last-release").to_dict()
    gate = auto_heal_gate(playbook, "high", approval_id="", within_maintenance_window=True)
    assert gate["allowed"] is False
    approved = auto_heal_gate(playbook, "high", approval_id="approved_manual_001", within_maintenance_window=True)
    assert approved["allowed"] is True
    assert rollback_guard(["rollback"], True, True)["allowed"] is True
    signals = [create_signal("gateway", "error_rate", 0.06, "release-center")]
    incident = detect_incident(signals, "release-center")["incident"]
    payload = build_healing_plan(incident, "approved_manual_001", True)
    assert payload["plan"]["dry_run"] is True
    assert payload["rollback"]["allowed"] is True
    path = write_healing_plan(payload["plan"], tmp_path)
    assert Path(path).exists()
    assert healing_readiness(payload["plan"])["allowed"] is True
    assert healing_readiness(payload["plan"], apply_requested=True)["allowed"] is False


def test_escalation_postmortem_audit(tmp_path):
    signals = [create_signal("gateway", "error_rate", 0.06, "core")]
    incident = detect_incident(signals, "core")["incident"]
    assert escalation_policy()["high"]["approval_required"] is True
    assert escalation_decision(incident)["dry_run"] is True
    assert notification_draft(incident)["send"] is False
    md = postmortem_markdown(incident)
    assert "Postmortem" in md
    path = write_postmortem(incident, root=tmp_path)
    assert Path(path).exists()
    audit = HealingAuditLog(tmp_path / "healing.db")
    event = audit.record("tester", "healing.plan", incident["id"])
    assert audit.list_events()[0]["id"] == event.id


def test_control_ui_routes(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert self_healing_status()["ok"] is True
    assert demo_signals()
    assert incident_demo()["detected"] is True
    demo = healing_plan_demo(str(tmp_path))
    assert Path(demo["plan_path"]).exists()
    assert Path(demo["postmortem_path"]).exists()
    assert self_healing_overview()["detected"]["detected"] is True
    assert "Self-Healing Operations" in render_healing_overview()
    assert "Incidents" in render_incidents_page()
    assert "Playbooks" in render_playbooks_page()
    assert "Policy" in render_policy_page()
    assert route_self_healing_status()["ok"] is True
    assert route_self_healing_overview()["status"]["ok"] is True
    assert route_signal_demo()["worst"] == "critical"
    assert route_incident_demo()["detected"] is True
    assert route_playbook_catalog()["validation"]["ok"] is True
    assert route_guardrail_policy()["rollback"]["allowed"] is True
    assert route_healing_plan_demo()["healing"]["plan"]["dry_run"] is True
    assert route_escalation_demo()["notification"]["send"] is False
    assert "markdown" in route_postmortem_demo()
    assert "events" in route_healing_audit()
    assert route_self_healing_page()["content_type"] == "text/html"
    assert route_self_healing_incidents_page()["content_type"] == "text/html"
    assert route_self_healing_playbooks_page()["content_type"] == "text/html"
    assert route_self_healing_policy_page()["content_type"] == "text/html"


def test_docs_scripts_assets_exist():
    root = Path(__file__).resolve().parents[1]
    for rel in [
        "scripts/self-healing/self-healing-status.sh",
        "scripts/self-healing/signal-demo.sh",
        "scripts/self-healing/incident-detect-demo.sh",
        "scripts/self-healing/playbook-catalog.sh",
        "scripts/self-healing/guardrail-policy.sh",
        "scripts/self-healing/healing-plan-demo.sh",
        "scripts/self-healing/escalation-demo.sh",
        "scripts/self-healing/postmortem-demo.sh",
        "scripts/self-healing/healing-audit.sh",
        "scripts/self-healing/self-healing-dashboard-export.sh",
        "docs/self-healing/SELF_HEALING_OPERATIONS_GUIDE.md",
        "docs/self-healing/HEALTH_SIGNALS_AND_INCIDENTS.md",
        "docs/self-healing/REMEDIATION_PLAYBOOKS.md",
        "docs/self-healing/SELF_HEALING_GUARDRAILS.md",
        "docs/self-healing/POSTMORTEM_TEMPLATE.md",
        "docs/requirements/NEXT_V30_SELF_HEALING_OPERATIONS_REQUIREMENTS.md",
        "assets/self-healing/self_healing_operations_features.json",
    ]:
        assert (root / rel).exists(), rel
