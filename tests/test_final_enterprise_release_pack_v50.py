from pathlib import Path
from zai_coder.final_enterprise_release_pack.models import ReleaseArtifact, FinalValidationGate, HermesAlignmentItem
from zai_coder.final_enterprise_release_pack.core import *
from zai_coder.final_enterprise_release_pack.routes import *

def test_models_validation():
    assert ReleaseArtifact("a","Artifact","docs","docs/x.md").validate() == []
    assert ReleaseArtifact("","","bad","secret/token").validate()
    assert FinalValidationGate("g","Gate","test","passed").validate() == []
    assert FinalValidationGate("","","bad","bad").validate()
    assert HermesAlignmentItem("h","Memory","memory").validate() == []
    assert HermesAlignmentItem("","","bad", safety_note="").validate()

def test_core_final_release():
    assert release_artifacts()
    assert final_validation_gates()
    assert hermes_alignment_items()
    assert validation_report()["ok"]
    score = final_readiness_scorecard()
    assert score["manual_release_review_required"] is True
    assert installer_manifest()["safe_defaults"]["production_launch"] is False
    assert "final_release" in dashboard_route_index()
    bundle = final_release_bundle()
    assert bundle["automatic_production_launch"] is False
    assert bundle["secrets_included"] is False
    assert bundle["requires_review"] is True

def test_exports(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert Path(write_final_release_export(tmp_path)).exists()
    assert Path(write_final_validation_report(tmp_path)).exists()
    demo = final_release_demo(str(tmp_path))
    assert Path(demo["export_path"]).exists()
    assert Path(demo["report_path"]).exists()

def test_routes():
    assert route_final_release_status()["ok"]
    assert route_final_release_overview()["validation"]["ok"]
    assert route_final_installer_manifest()["safe_defaults"]["production_launch"] is False
    assert route_final_docs_index()["artifacts"]
    assert "core" in route_final_dashboard_index()
    assert route_final_validation_report()["scorecard"]["manual_release_review_required"]
    assert route_final_release_notes()["release"] == "v50"
    assert route_final_go_live_checklist()["automatic_launch"] is False
    assert "export_path" in route_final_release_export()
    assert "export_path" in route_final_release_demo()
    assert route_final_release_page()["content_type"] == "text/html"
    assert route_final_docs_page()["content_type"] == "text/html"
    assert route_final_dashboards_page()["content_type"] == "text/html"
    assert route_final_validation_page()["content_type"] == "text/html"
    assert route_final_go_live_page()["content_type"] == "text/html"

def test_docs_scripts_assets_exist():
    root = Path(__file__).resolve().parents[1]
    for rel in [
        "scripts/final-release/final-release-status.sh",
        "scripts/final-release/final-installer-manifest.sh",
        "scripts/final-release/final-docs-index.sh",
        "scripts/final-release/final-dashboard-index.sh",
        "scripts/final-release/final-validation-report.sh",
        "scripts/final-release/final-release-notes.sh",
        "scripts/final-release/final-go-live-checklist.sh",
        "scripts/final-release/final-release-export.sh",
        "scripts/final-release/final-release-demo.sh",
        "scripts/final-release/final-dashboard-export.sh",
        "docs/final-release/FINAL_ENTERPRISE_RELEASE_PACK_GUIDE.md",
        "docs/final-release/FINAL_DOCUMENTATION_INDEX.md",
        "docs/final-release/DASHBOARD_ROUTE_INDEX.md",
        "docs/final-release/SECURITY_PRIVACY_COMPLIANCE_SUMMARY.md",
        "docs/final-release/MIGRATION_GUIDE.md",
        "docs/final-release/ROLLBACK_GUIDE.md",
        "docs/final-release/RELEASE_NOTES_V50.md",
        "docs/final-release/FINAL_GO_LIVE_CHECKLIST.md",
        "docs/hermes-agent-alignment/HERMES_AGENT_ALIGNMENT.md",
        "docs/requirements/NEXT_V50_FINAL_ENTERPRISE_RELEASE_PACK_REQUIREMENTS.md",
        "assets/final-release/final_enterprise_release_pack_features.json",
    ]:
        assert (root / rel).exists(), rel
