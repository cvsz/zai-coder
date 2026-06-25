from pathlib import Path
from zai_coder.production_readiness_go_live_command_center.models import ReadinessGate, GoLiveChecklistItem, LaunchAction, RollbackPlan
from zai_coder.production_readiness_go_live_command_center.core import *
from zai_coder.production_readiness_go_live_command_center.routes import *

def test_models_validation():
    assert ReadinessGate("g","Gate","qa").validate() == []
    assert ReadinessGate("","","bad", status="bad").validate()
    assert GoLiveChecklistItem("c","Checklist","owner").validate() == []
    assert GoLiveChecklistItem("","","", phase="bad", manual_approval=False).validate()
    assert LaunchAction("a","Action","monitor").validate() == []
    assert LaunchAction("","","bad", status="bad", dry_run=False).validate()
    assert RollbackPlan("r","Rollback","trigger").validate() == []
    assert RollbackPlan("","","", status="bad", dry_run=False).validate()

def test_core_go_live():
    assert readiness_gates()
    assert go_live_checklist()
    assert launch_actions()
    assert rollback_plans()
    assert validation_report()["ok"]
    assert release_readiness_scorecard()["manual_approval_required"]
    assert launch_command_center()["execute_launch"] is False
    assert manual_approval_gate()["apply_approval"] is False
    assert rollback_plan()["execute_rollback"] is False
    bundle = launch_evidence_bundle()
    assert bundle["automatic_launch"] is False
    assert bundle["production_mutation"] is False
    assert bundle["requires_review"] is True

def test_exports(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert Path(write_launch_evidence(tmp_path)).exists()
    assert Path(write_launch_report(tmp_path)).exists()
    demo = go_live_demo(str(tmp_path))
    assert Path(demo["evidence_path"]).exists()
    assert Path(demo["report_path"]).exists()

def test_routes():
    assert route_go_live_status()["ok"]
    assert route_go_live_overview()["validation"]["ok"]
    assert route_readiness_gates()["scorecard"]["manual_approval_required"]
    assert route_go_live_checklist()["checklist"]
    assert route_launch_command_center()["execute_launch"] is False
    assert route_manual_approval_gate()["apply_approval"] is False
    assert route_rollback_plan()["execute_rollback"] is False
    assert "evidence_path" in route_launch_evidence_export()
    assert "evidence_path" in route_go_live_demo()
    assert route_go_live_page()["content_type"] == "text/html"
    assert route_go_live_gates_page()["content_type"] == "text/html"
    assert route_go_live_checklist_page()["content_type"] == "text/html"
    assert route_go_live_command_center_page()["content_type"] == "text/html"
    assert route_go_live_rollback_page()["content_type"] == "text/html"

def test_docs_scripts_assets_exist():
    root = Path(__file__).resolve().parents[1]
    for rel in [
        "scripts/go-live-command-center/go-live-status.sh",
        "scripts/go-live-command-center/readiness-gates.sh",
        "scripts/go-live-command-center/go-live-checklist.sh",
        "scripts/go-live-command-center/launch-command-center.sh",
        "scripts/go-live-command-center/manual-approval-gate.sh",
        "scripts/go-live-command-center/rollback-plan.sh",
        "scripts/go-live-command-center/launch-evidence-export.sh",
        "scripts/go-live-command-center/go-live-demo.sh",
        "scripts/go-live-command-center/go-live-dashboard-export.sh",
        "docs/go-live-command-center/PRODUCTION_READINESS_GO_LIVE_COMMAND_CENTER_GUIDE.md",
        "docs/go-live-command-center/READINESS_GATES.md",
        "docs/go-live-command-center/GO_LIVE_CHECKLIST.md",
        "docs/go-live-command-center/LAUNCH_COMMAND_CENTER.md",
        "docs/go-live-command-center/ROLLBACK_PLAN.md",
        "docs/go-live-command-center/LAUNCH_EVIDENCE_POLICY.md",
        "docs/requirements/NEXT_V49_PRODUCTION_READINESS_GO_LIVE_COMMAND_CENTER_REQUIREMENTS.md",
        "assets/go-live-command-center/production_readiness_go_live_features.json",
    ]:
        assert (root / rel).exists(), rel
