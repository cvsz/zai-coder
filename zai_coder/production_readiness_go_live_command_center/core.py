from __future__ import annotations
import json
from pathlib import Path
from .models import ReadinessGate, GoLiveChecklistItem, LaunchAction, RollbackPlan

GATES = [
    ReadinessGate("gate_qa", "QA test suite passed", "qa", True, "passed", "BUILD_REPORT_V48"),
    ReadinessGate("gate_security", "Security review complete", "security", True, "passed", "security/evidence"),
    ReadinessGate("gate_identity", "Identity access review complete", "identity", True, "passed", "identity/evidence"),
    ReadinessGate("gate_scalability", "Scalability plan reviewed", "scalability", True, "passed", "scalability/evidence"),
    ReadinessGate("gate_docs", "Operator and developer docs ready", "docs", True, "passed", "docs/"),
    ReadinessGate("gate_rollback", "Rollback plan reviewed", "rollback", True, "pending", "go-live/rollback"),
    ReadinessGate("gate_manual", "Final human go-live approval", "approval", True, "pending", "go-live/approval"),
]
CHECKLIST = [
    GoLiveChecklistItem("gl_preflight", "Run final preflight checks", "release-owner", "preflight", True, True),
    GoLiveChecklistItem("gl_artifacts", "Verify release artifacts and checksums", "release-owner", "preflight", True, True),
    GoLiveChecklistItem("gl_comms", "Prepare launch communication", "customer-success", "launch", False, True),
    GoLiveChecklistItem("gl_monitoring", "Confirm monitoring owner rotation", "ops-owner", "monitoring", False, True),
    GoLiveChecklistItem("gl_rollback", "Confirm rollback decision path", "incident-owner", "rollback", False, True),
]
ACTIONS = [
    LaunchAction("act_release_review", "Review final release bundle", "deploy_review", "ready", True),
    LaunchAction("act_traffic_review", "Review traffic routing plan", "traffic_review", "planned", True),
    LaunchAction("act_monitor", "Start launch monitoring plan", "monitor", "planned", True),
    LaunchAction("act_handoff", "Operator handoff briefing", "handoff", "planned", True),
]
ROLLBACKS = [
    RollbackPlan("rb_release", "Release rollback plan", "quality gate failed", "review", True),
    RollbackPlan("rb_traffic", "Traffic rollback plan", "latency budget exceeded", "review", True),
    RollbackPlan("rb_security", "Security hold plan", "critical security review finding", "draft", True),
]

def readiness_gates(): return [g.to_dict() for g in GATES]
def go_live_checklist(): return [c.to_dict() for c in CHECKLIST]
def launch_actions(): return [a.to_dict() for a in ACTIONS]
def rollback_plans(): return [r.to_dict() for r in ROLLBACKS]

def validation_report():
    rows = [*GATES, *CHECKLIST, *ACTIONS, *ROLLBACKS]
    reports = [{"id": x.id, "issues": x.validate()} for x in rows]
    return {"ok": all(not r["issues"] for r in reports), "reports": reports}

def release_readiness_scorecard():
    required = [g for g in GATES if g.required]
    passed = [g for g in required if g.status == "passed"]
    pending = [g for g in required if g.status == "pending"]
    blocked = [g.to_dict() for g in required if g.status in {"failed","blocked"}]
    score = round(len(passed) * 100 / len(required), 2)
    return {"score": score, "required": len(required), "passed": len(passed), "pending": len(pending), "blocked": blocked, "ready": score == 100 and not blocked, "manual_approval_required": True}

def launch_command_center():
    return {"dry_run": True, "actions": launch_actions(), "scorecard": release_readiness_scorecard(), "checklist": go_live_checklist(), "execute_launch": False, "requires_manual_approval": True}

def manual_approval_gate(approver="release-owner"):
    score = release_readiness_scorecard()
    blocked = []
    if not score["ready"]: blocked.append("readiness scorecard is not complete")
    if approver not in {"release-owner","platform-owner","security-owner"}: blocked.append("approver is not authorized for final approval")
    return {"dry_run": True, "approver": approver, "allowed": not blocked, "blocked": blocked, "apply_approval": False}

def rollback_plan(plan_id="rb_release"):
    plan = next((p for p in ROLLBACKS if p.id == plan_id), None)
    if not plan: raise ValueError(f"unknown rollback plan: {plan_id}")
    return {"dry_run": True, "plan": plan.to_dict(), "steps": ["declare hold", "notify owners", "restore previous stable artifact", "verify health", "write incident summary"], "execute_rollback": False}

def launch_evidence_bundle():
    return {"kind": "zai-production-readiness-go-live-evidence", "version": "1.0", "readiness_gates": readiness_gates(), "checklist": go_live_checklist(), "actions": launch_actions(), "rollback_plans": rollback_plans(), "scorecard": release_readiness_scorecard(), "command_center": launch_command_center(), "approval_gate": manual_approval_gate(), "validation": validation_report(), "automatic_launch": False, "production_mutation": False, "requires_review": True}

def write_launch_evidence(root=".", out="go-live/evidence/launch-evidence.json"):
    path = Path(root) / out
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(launch_evidence_bundle(), indent=2, sort_keys=True), encoding="utf-8")
    return str(path)

def write_launch_report(root=".", out="go-live/reports/go-live-command-center-report.md"):
    path = Path(root) / out
    path.parent.mkdir(parents=True, exist_ok=True)
    gates = "\n".join(f"- {g.title} [{g.category} / {g.status}]" for g in GATES)
    checklist = "\n".join(f"- {i.title} [{i.phase} / done={i.done}]" for i in CHECKLIST)
    path.write_text(f"# Production Readiness and Go Live Command Center Report\n\n## Readiness Gates\n\n{gates}\n\n## Checklist\n\n{checklist}\n\n## Safety\n\n- Manual approval gates required.\n- No automatic production launch.\n- Rollback plans are review-first.\n", encoding="utf-8")
    return str(path)

def go_live_status(): return {"ok": True, "systems": ["readiness_gates","go_live_checklist","launch_command_center","manual_approval_gate","rollback_plans","launch_evidence","release_scorecard","dashboard_routes"]}
def go_live_overview(): return {"status": go_live_status(), "gates": readiness_gates(), "checklist": go_live_checklist(), "actions": launch_actions(), "scorecard": release_readiness_scorecard(), "validation": validation_report()}
def go_live_demo(root="."):
    evidence = write_launch_evidence(root)
    report = write_launch_report(root)
    return {"evidence_path": evidence, "report_path": report, "command_center": launch_command_center(), "rollback": rollback_plan(), "bundle": launch_evidence_bundle()}
