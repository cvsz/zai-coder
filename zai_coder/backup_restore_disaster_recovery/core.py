from __future__ import annotations
import json
from pathlib import Path
from .models import BackupPlan, RestoreDrill, RecoveryTarget, DrScenario

BACKUP_PLANS = [
    BackupPlan("bp_config", "Configuration backup plan", "local/config", "daily", 14, "review", True),
    BackupPlan("bp_sqlite", "Local SQLite backup plan", "data/*.sqlite", "daily", 7, "review", True),
    BackupPlan("bp_exports", "Evidence export backup plan", "exports/", "weekly", 30, "draft", True),
]

SCENARIOS = [
    DrScenario("dr_operator_error", "Operator error recovery", "operator_error", "medium"),
    DrScenario("dr_deploy_regression", "Deployment regression rollback", "deployment_regression", "high"),
    DrScenario("dr_dependency_failure", "Dependency failure continuity", "dependency_failure", "high"),
]

TARGETS = [
    RecoveryTarget("rto_control", "control-plane", 15, 60, "critical"),
    RecoveryTarget("rto_docs", "developer-docs", 240, 480, "normal"),
    RecoveryTarget("rto_exports", "evidence-exports", 60, 240, "high"),
]

DRILLS = [
    RestoreDrill("drill_config_preview", "bp_config", "dr_operator_error", "preview", "planned", True),
    RestoreDrill("drill_sqlite_tabletop", "bp_sqlite", "dr_deploy_regression", "tabletop", "planned", True),
    RestoreDrill("drill_exports_verify", "bp_exports", "dr_dependency_failure", "verification", "planned", True),
]

def backup_plan_registry(): return [p.to_dict() for p in BACKUP_PLANS]
def restore_drill_registry(): return [d.to_dict() for d in DRILLS]
def recovery_targets(): return [t.to_dict() for t in TARGETS]
def dr_scenarios(): return [s.to_dict() for s in SCENARIOS]

def validation_report() -> dict:
    rows = [*BACKUP_PLANS, *SCENARIOS, *TARGETS, *DRILLS]
    reports = [{"id": x.id, "issues": x.validate()} for x in rows]
    return {"ok": all(not r["issues"] for r in reports), "reports": reports}

def backup_plan(plan_id="bp_config") -> dict:
    plan = next((p for p in BACKUP_PLANS if p.id == plan_id), None)
    if not plan: raise ValueError(f"unknown backup plan: {plan_id}")
    return {"dry_run": True, "plan": plan.to_dict(), "steps": ["validate target", "estimate size", "write backup manifest", "review retention"], "write_backup": False}

def restore_drill_preview(drill_id="drill_config_preview") -> dict:
    drill = next((d for d in DRILLS if d.id == drill_id), None)
    if not drill: raise ValueError(f"unknown drill: {drill_id}")
    scenario = next((s for s in SCENARIOS if s.id == drill.scenario_id), None)
    return {"dry_run": True, "drill": drill.to_dict(), "scenario": scenario.to_dict() if scenario else None, "steps": ["load backup manifest", "verify target sandbox", "simulate restore", "compare checksums", "write evidence"], "perform_restore": False}

def readiness_gate(metrics: dict | None = None) -> dict:
    metrics = metrics or {"backup_plan_count": len(BACKUP_PLANS), "restore_drill_count": len(DRILLS), "critical_rto_defined": 1, "blocked_drills": 0}
    results = [
        {"id": "backup-plans", "passed": metrics["backup_plan_count"] >= 1, "value": metrics["backup_plan_count"]},
        {"id": "restore-drills", "passed": metrics["restore_drill_count"] >= 1, "value": metrics["restore_drill_count"]},
        {"id": "critical-rto", "passed": metrics["critical_rto_defined"] >= 1, "value": metrics["critical_rto_defined"]},
        {"id": "blocked-drills", "passed": metrics["blocked_drills"] == 0, "value": metrics["blocked_drills"]},
    ]
    return {"ok": all(r["passed"] for r in results), "results": results, "dry_run": True}

def recovery_evidence_bundle() -> dict:
    return {
        "kind": "zai-backup-restore-dr-evidence",
        "version": "1.0",
        "backup_plans": backup_plan_registry(),
        "restore_drills": restore_drill_registry(),
        "recovery_targets": recovery_targets(),
        "scenarios": dr_scenarios(),
        "validation": validation_report(),
        "restore_preview": restore_drill_preview(),
        "readiness_gate": readiness_gate(),
        "external_upload": False,
        "requires_review": True,
    }

def write_dr_evidence(root=".", out="dr/evidence/dr-evidence.json") -> str:
    path = Path(root) / out
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(recovery_evidence_bundle(), indent=2, sort_keys=True), encoding="utf-8")
    return str(path)

def write_dr_report(root=".", out="dr/reports/disaster-recovery-report.md") -> str:
    path = Path(root) / out
    path.parent.mkdir(parents=True, exist_ok=True)
    plans = "\n".join(f"- {p.name} [{p.cadence} / retention={p.retention_days}d / dry_run={p.dry_run}]" for p in BACKUP_PLANS)
    targets = "\n".join(f"- {t.service}: RPO={t.rpo_minutes}m RTO={t.rto_minutes}m [{t.priority}]" for t in TARGETS)
    path.write_text(f"# Backup Restore and Disaster Recovery Report\n\n## Backup Plans\n\n{plans}\n\n## Recovery Targets\n\n{targets}\n\n## Safety\n\n- Restore workflows are preview-only by default.\n- No direct production restore.\n- Evidence export is local-only.\n", encoding="utf-8")
    return str(path)

def dr_status():
    return {"ok": True, "systems": ["backup_plan_registry","restore_drill_preview","rpo_rto_targets","dr_scenarios","readiness_gate","recovery_evidence","dashboard_routes"]}

def dr_overview():
    return {"status": dr_status(), "backup_plans": backup_plan_registry(), "restore_drills": restore_drill_registry(), "targets": recovery_targets(), "scenarios": dr_scenarios(), "validation": validation_report(), "readiness": readiness_gate()}

def dr_demo(root="."):
    evidence_path = write_dr_evidence(root)
    report_path = write_dr_report(root)
    return {"evidence_path": evidence_path, "report_path": report_path, "backup_plan": backup_plan(), "restore_preview": restore_drill_preview(), "bundle": recovery_evidence_bundle()}
