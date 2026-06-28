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

def run_sast_scan(root: str = ".") -> list[dict]:
    import os
    import re
    findings = []
    secret_pattern = re.compile(r'(?i)(password|api_key|secret|token)\s*=\s*[\'"][^\'"]+[\'"]')
    
    for dirpath, _, filenames in os.walk(root):
        if "/.git" in dirpath or "/__pycache__" in dirpath:
            continue
        for filename in filenames:
            if not filename.endswith(".py"):
                continue
            filepath = os.path.join(dirpath, filename)
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                    matches = secret_pattern.findall(content)
                    if matches:
                        findings.append({
                            "file": filepath,
                            "type": "hardcoded_secret",
                            "severity": "high",
                            "message": f"Found potential hardcoded secret keys: {matches}"
                        })
            except Exception:
                pass
    return findings

def threat_signal_registry(execute: bool = False):
    signals = [s.to_dict() for s in SIGNALS]
    if execute:
        # Run real SAST checks instead of just static facade
        findings = run_sast_scan()
        if findings:
            signals.append({
                "id": "sig_sast_findings",
                "title": f"SAST identified {len(findings)} potential issues",
                "signal_type": "sast_alert",
                "source": "local-sast-scanner",
                "severity": "high",
                "status": "open",
                "raw_findings": findings
            })
    return signals

def policy_alert_catalog(execute: bool = False):
    alerts = [a.to_dict() for a in ALERTS]
    if execute:
        findings = run_sast_scan()
        if findings:
            alerts.append({
                "id": "alert_sast_secrets",
                "policy_id": "policy-no-hardcoded-secrets",
                "title": "Hardcoded secrets detected",
                "severity": "high",
                "action": "create_incident_plan",
                "status": "open"
            })
    return alerts

def incident_workflow_plans(): return [i.to_dict() for i in INCIDENTS]
def security_evidence_catalog(): return [e.to_dict() for e in EVIDENCE]

def validation_report() -> dict:
    rows = [*SIGNALS, *ALERTS, *INCIDENTS, *EVIDENCE]
    reports = [{"id": x.id, "issues": x.validate()} for x in rows]
    return {"ok": all(not r["issues"] for r in reports), "reports": reports}

def risk_scorecard(execute: bool = False) -> dict:
    signals = threat_signal_registry(execute)
    alerts = policy_alert_catalog(execute)
    signal_score = sum(SEVERITY_WEIGHT.get(s.get("severity", "low"), 1) for s in signals if s.get("status") in {"open", "triaged", "monitoring"})
    alert_score = sum(SEVERITY_WEIGHT.get(a.get("severity", "low"), 1) for a in alerts if a.get("status") in {"open", "in_review"})
    incident_score = sum(SEVERITY_WEIGHT[i.severity] for i in INCIDENTS if i.status in {"draft", "review"})
    total = signal_score + alert_score + incident_score
    posture = "critical" if total >= 20 else "elevated" if total >= 12 else "watch" if total >= 6 else "normal"
    return {"score": total, "posture": posture, "signals": signal_score, "alerts": alert_score, "incidents": incident_score, "dry_run": not execute}

def alert_review_queue(execute: bool = False) -> dict:
    queue = []
    for alert in policy_alert_catalog(execute):
        if alert.get("status") in {"open", "in_review"}:
            queue.append({"id": alert["id"], "title": alert["title"], "severity": alert["severity"], "action": alert["action"], "review_required": True})
    return {"queue": queue, "count": len(queue), "auto_blocking": False, "requires_human_review": True}

def incident_workflow_plan(plan_id="inc_access_review") -> dict:
    plan = next((p for p in INCIDENTS if p.id == plan_id), None)
    if not plan: raise ValueError(f"unknown incident plan: {plan_id}")
    return {"dry_run": True, "plan": plan.to_dict(), "steps": ["assign owner", "collect redacted evidence", "review impact", "approve response plan", "write closure report"], "execute_response": False}

def security_evidence_bundle(execute: bool = False) -> dict:
    return {
        "kind": "zai-security-ops-evidence",
        "version": "1.0",
        "signals": threat_signal_registry(execute),
        "alerts": policy_alert_catalog(execute),
        "incidents": incident_workflow_plans(),
        "evidence": security_evidence_catalog(),
        "validation": validation_report(),
        "risk": risk_scorecard(execute),
        "alert_queue": alert_review_queue(execute),
        "external_publish": False,
        "active_blocking": False,
        "requires_review": True,
    }

def write_security_evidence(root=".", out="security/evidence/security-ops-evidence.json", execute: bool = False) -> str:
    path = Path(root) / out
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(security_evidence_bundle(execute), indent=2, sort_keys=True), encoding="utf-8")
    return str(path)

def write_security_report(root=".", out="security/reports/security-ops-report.md", execute: bool = False) -> str:
    path = Path(root) / out
    path.parent.mkdir(parents=True, exist_ok=True)
    signals = "\n".join(f"- {s.get('title')} [{s.get('signal_type')} / {s.get('severity')} / {s.get('status')}]" for s in threat_signal_registry(execute))
    alerts = "\n".join(f"- {a.get('title')} [{a.get('severity')} / {a.get('action')} / {a.get('status')}]" for a in policy_alert_catalog(execute))
    path.write_text(f"# Security Operations and Threat Monitoring Report\n\n## Signals\n\n{signals}\n\n## Alerts\n\n{alerts}\n\n## Safety\n\n- No secret leakage.\n- No active blocking automation by default.\n- Incident workflows are plan-only.\n", encoding="utf-8")
    return str(path)

def security_ops_status():
    return {"ok": True, "systems": ["security_dashboard","threat_signal_registry","policy_alerts","incident_workflow_plans","risk_scorecard","alert_review_queue","security_evidence","dashboard_routes"]}

def security_ops_overview(execute: bool = False):
    return {"status": security_ops_status(), "signals": threat_signal_registry(execute), "alerts": policy_alert_catalog(execute), "incidents": incident_workflow_plans(), "validation": validation_report(), "risk": risk_scorecard(execute), "queue": alert_review_queue(execute)}

def security_ops_demo(root=".", execute: bool = False):
    evidence_path = write_security_evidence(root, execute=execute)
    report_path = write_security_report(root, execute=execute)
    return {"evidence_path": evidence_path, "report_path": report_path, "workflow": incident_workflow_plan(), "bundle": security_evidence_bundle(execute)}
