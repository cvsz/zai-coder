from __future__ import annotations
import json
from pathlib import Path
from .models import ThreatSignal, PolicyAlert, IncidentPlan, SecurityEvidence

SIGNALS = [
    ThreatSignal("sig_auth_review", "Unusual local auth retry pattern", "auth_anomaly", "local-auth-log", "medium", "open"),
    ThreatSignal("sig_policy_drift", "Cloud policy review requested", "policy_drift", "config-snapshot", "high", "triaged"),
    ThreatSignal("sig_dependency", "Dependency review advisory", "dependency_alert", "local-dependency-index", "medium", "monitoring"),
    ThreatSignal("sig_availability", "Service health variance", "availability", "local-health-summary", "low", "open"),
]

ALERTS = [
    PolicyAlert("alert_mfa_review", "policy-access-review", "Access policy review required", "high", "create_incident_plan", "open"),
    PolicyAlert("alert_dependency_review", "policy-dependency-review", "Dependency update review required", "medium", "review", "in_review"),
    PolicyAlert("alert_config_snapshot", "policy-config-review", "Configuration snapshot review due", "medium", "notify_owner", "open"),
]

INCIDENTS = [
    IncidentPlan("inc_access_review", "Access review workflow plan", "access_review", "high", "draft", True),
    IncidentPlan("inc_policy_drift", "Policy drift review workflow", "policy_drift", "high", "review", True),
    IncidentPlan("inc_availability", "Availability review workflow", "availability_review", "medium", "draft", True),
]

EVIDENCE = [
    SecurityEvidence("ev_signal_summary", "signal_summary", "Threat signal summary", True, "ready"),
    SecurityEvidence("ev_alert_summary", "alert_summary", "Policy alert summary", True, "ready"),
    SecurityEvidence("ev_incident_plan", "incident_plan", "Incident workflow plan evidence", True, "review"),
]

SEVERITY_WEIGHT = {"low": 1, "medium": 2, "high": 3, "critical": 5}

def threat_signal_registry(): return [s.to_dict() for s in SIGNALS]
def policy_alert_catalog(): return [a.to_dict() for a in ALERTS]
def incident_workflow_plans(): return [i.to_dict() for i in INCIDENTS]
def security_evidence_catalog(): return [e.to_dict() for e in EVIDENCE]

def validation_report() -> dict:
    rows = [*SIGNALS, *ALERTS, *INCIDENTS, *EVIDENCE]
    reports = [{"id": x.id, "issues": x.validate()} for x in rows]
    return {"ok": all(not r["issues"] for r in reports), "reports": reports}

def risk_scorecard() -> dict:
    signal_score = sum(SEVERITY_WEIGHT[s.severity] for s in SIGNALS if s.status in {"open", "triaged", "monitoring"})
    alert_score = sum(SEVERITY_WEIGHT[a.severity] for a in ALERTS if a.status in {"open", "in_review"})
    incident_score = sum(SEVERITY_WEIGHT[i.severity] for i in INCIDENTS if i.status in {"draft", "review"})
    total = signal_score + alert_score + incident_score
    posture = "critical" if total >= 20 else "elevated" if total >= 12 else "watch" if total >= 6 else "normal"
    return {"score": total, "posture": posture, "signals": signal_score, "alerts": alert_score, "incidents": incident_score, "dry_run": True}

def alert_review_queue() -> dict:
    queue = []
    for alert in ALERTS:
        if alert.status in {"open", "in_review"}:
            queue.append({"id": alert.id, "title": alert.title, "severity": alert.severity, "action": alert.action, "review_required": True})
    return {"queue": queue, "count": len(queue), "auto_blocking": False, "requires_human_review": True}

def incident_workflow_plan(plan_id="inc_access_review") -> dict:
    plan = next((p for p in INCIDENTS if p.id == plan_id), None)
    if not plan: raise ValueError(f"unknown incident plan: {plan_id}")
    return {"dry_run": True, "plan": plan.to_dict(), "steps": ["assign owner", "collect redacted evidence", "review impact", "approve response plan", "write closure report"], "execute_response": False}

def security_evidence_bundle() -> dict:
    return {
        "kind": "zai-security-ops-evidence",
        "version": "1.0",
        "signals": threat_signal_registry(),
        "alerts": policy_alert_catalog(),
        "incidents": incident_workflow_plans(),
        "evidence": security_evidence_catalog(),
        "validation": validation_report(),
        "risk": risk_scorecard(),
        "alert_queue": alert_review_queue(),
        "external_publish": False,
        "active_blocking": False,
        "requires_review": True,
    }

def write_security_evidence(root=".", out="security/evidence/security-ops-evidence.json") -> str:
    path = Path(root) / out
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(security_evidence_bundle(), indent=2, sort_keys=True), encoding="utf-8")
    return str(path)

def write_security_report(root=".", out="security/reports/security-ops-report.md") -> str:
    path = Path(root) / out
    path.parent.mkdir(parents=True, exist_ok=True)
    signals = "\n".join(f"- {s.title} [{s.signal_type} / {s.severity} / {s.status}]" for s in SIGNALS)
    alerts = "\n".join(f"- {a.title} [{a.severity} / {a.action} / {a.status}]" for a in ALERTS)
    path.write_text(f"# Security Operations and Threat Monitoring Report\n\n## Signals\n\n{signals}\n\n## Alerts\n\n{alerts}\n\n## Safety\n\n- No secret leakage.\n- No active blocking automation by default.\n- Incident workflows are plan-only.\n", encoding="utf-8")
    return str(path)

def security_ops_status():
    return {"ok": True, "systems": ["security_dashboard","threat_signal_registry","policy_alerts","incident_workflow_plans","risk_scorecard","alert_review_queue","security_evidence","dashboard_routes"]}

def security_ops_overview():
    return {"status": security_ops_status(), "signals": threat_signal_registry(), "alerts": policy_alert_catalog(), "incidents": incident_workflow_plans(), "validation": validation_report(), "risk": risk_scorecard(), "queue": alert_review_queue()}

def security_ops_demo(root="."):
    evidence_path = write_security_evidence(root)
    report_path = write_security_report(root)
    return {"evidence_path": evidence_path, "report_path": report_path, "workflow": incident_workflow_plan(), "bundle": security_evidence_bundle()}
