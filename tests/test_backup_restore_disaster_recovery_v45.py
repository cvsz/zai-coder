from pathlib import Path
from zai_coder.backup_restore_disaster_recovery.models import BackupPlan, RestoreDrill, RecoveryTarget, DrScenario
from zai_coder.backup_restore_disaster_recovery.core import *
from zai_coder.backup_restore_disaster_recovery.routes import *

def test_models_validation():
    assert BackupPlan("b","Backup","target").validate() == []
    assert BackupPlan("","","secret token", cadence="bad", retention_days="bad", status="bad", dry_run=False).validate()
    assert RestoreDrill("d","b","s").validate() == []
    assert RestoreDrill("","","", drill_type="bad", status="bad", dry_run=False).validate()
    assert RecoveryTarget("r","svc",15,60).validate() == []
    assert RecoveryTarget("","",-1,"bad", priority="bad").validate()
    assert DrScenario("s","Scenario","data_loss").validate() == []
    assert DrScenario("","","bad", severity="bad").validate()

def test_core_dr():
    assert backup_plan_registry()
    assert restore_drill_registry()
    assert recovery_targets()
    assert dr_scenarios()
    assert validation_report()["ok"]
    assert backup_plan()["dry_run"]
    assert restore_drill_preview()["perform_restore"] is False
    assert readiness_gate()["ok"]
    assert recovery_evidence_bundle()["requires_review"] is True

def test_exports(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert Path(write_dr_evidence(tmp_path)).exists()
    assert Path(write_dr_report(tmp_path)).exists()
    demo = dr_demo(str(tmp_path))
    assert Path(demo["evidence_path"]).exists()
    assert Path(demo["report_path"]).exists()

def test_routes():
    assert route_dr_status()["ok"]
    assert route_dr_overview()["validation"]["ok"]
    assert route_backup_plan()["write_backup"] is False
    assert route_restore_drill_preview()["perform_restore"] is False
    assert route_rpo_rto_targets()["targets"]
    assert route_dr_scenarios()["scenarios"]
    assert "evidence_path" in route_recovery_evidence()
    assert "evidence_path" in route_dr_demo()
    assert route_dr_page()["content_type"] == "text/html"
    assert route_dr_backups_page()["content_type"] == "text/html"
    assert route_dr_restore_drills_page()["content_type"] == "text/html"
    assert route_dr_rpo_rto_page()["content_type"] == "text/html"
    assert route_dr_evidence_page()["content_type"] == "text/html"

def test_docs_scripts_assets_exist():
    root = Path(__file__).resolve().parents[1]
    for rel in [
        "scripts/disaster-recovery/dr-status.sh",
        "scripts/disaster-recovery/backup-plan.sh",
        "scripts/disaster-recovery/restore-drill-preview.sh",
        "scripts/disaster-recovery/rpo-rto-targets.sh",
        "scripts/disaster-recovery/dr-scenarios.sh",
        "scripts/disaster-recovery/recovery-evidence.sh",
        "scripts/disaster-recovery/dr-demo.sh",
        "scripts/disaster-recovery/dr-dashboard-export.sh",
        "docs/disaster-recovery/BACKUP_RESTORE_DISASTER_RECOVERY_GUIDE.md",
        "docs/disaster-recovery/BACKUP_PLAN_REGISTRY.md",
        "docs/disaster-recovery/RESTORE_DRILL_POLICY.md",
        "docs/disaster-recovery/RPO_RTO_TARGETS.md",
        "docs/disaster-recovery/RECOVERY_EVIDENCE_POLICY.md",
        "docs/requirements/NEXT_V45_BACKUP_RESTORE_DISASTER_RECOVERY_REQUIREMENTS.md",
        "assets/disaster-recovery/backup_restore_disaster_recovery_features.json",
    ]:
        assert (root / rel).exists(), rel
