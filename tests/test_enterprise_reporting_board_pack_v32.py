from pathlib import Path
import tempfile

from zai_coder.enterprise_reporting_board_pack.models import KPI, BoardDecision, BoardRisk, ReportSection, BoardPack
from zai_coder.enterprise_reporting_board_pack.kpis import kpi_snapshot, kpi_validation_report, kpi_scorecard
from zai_coder.enterprise_reporting_board_pack.decisions import decision_register, risk_register, board_register_validation, board_action_summary
from zai_coder.enterprise_reporting_board_pack.narrative import executive_summary, investor_update, operations_update, compliance_update, narrative_bundle
from zai_coder.enterprise_reporting_board_pack.sections import board_sections
from zai_coder.enterprise_reporting_board_pack.builder import build_board_pack, board_pack_markdown, export_board_pack, export_bundle_manifest
from zai_coder.enterprise_reporting_board_pack.validation import board_pack_safety_gate, board_pack_quality_check
from zai_coder.enterprise_reporting_board_pack.audit import ReportingAuditLog
from zai_coder.enterprise_reporting_board_pack.control import reporting_status, board_pack_demo, reporting_overview
from zai_coder.enterprise_reporting_board_pack.ui.pages import render_board_overview_page, render_kpis_page, render_decisions_page, render_risks_page
from zai_coder.enterprise_reporting_board_pack.routes import (
    route_board_pack_status,
    route_board_pack_overview,
    route_kpi_snapshot,
    route_board_registers,
    route_narrative_bundle,
    route_board_pack_demo,
    route_board_pack_markdown,
    route_board_pack_safety,
    route_reporting_audit,
    route_board_pack_page,
    route_board_kpis_page,
    route_board_decisions_page,
    route_board_risks_page,
)


def test_models_validation():
    assert KPI("k", "KPI", 1, "count").validate() == []
    assert KPI("", "", -1, "", trend="bad").validate()
    assert BoardDecision("d", "Decision", "Owner").validate() == []
    assert BoardDecision("", "", "", status="bad", decision_type="bad").validate()
    assert BoardRisk("r", "Risk", "high", "Owner", "Mitigate").validate() == []
    assert BoardRisk("", "", "bad", "", "", status="bad").validate()
    assert ReportSection("s", "Section", "Body").validate() == []
    assert ReportSection("", "", "x").validate()


def test_kpis_decisions_narratives():
    assert kpi_snapshot()
    assert kpi_validation_report()["ok"] is True
    scorecard = kpi_scorecard()
    assert scorecard["counts"]["green"] >= 1
    assert decision_register()
    assert risk_register()
    assert board_register_validation()["ok"] is True
    summary = board_action_summary()
    assert summary["counts"]["decisions"] >= 1
    assert "ZAI Coder Control Plane" in executive_summary("Q1")
    assert "investor update" in investor_update("Q1").lower()
    assert "Operations update" in operations_update()
    assert "Compliance update" in compliance_update()
    assert narrative_bundle("Q1")["safe_disclaimer"]


def test_board_pack_builder_validation_export(tmp_path):
    sections = board_sections("Q1")
    assert len(sections) >= 4
    pack = build_board_pack("Q1")
    assert pack.validate() == []
    md = board_pack_markdown(pack)
    assert "KPI Appendix" in md
    exports = export_board_pack(pack, tmp_path)
    assert Path(exports["json"]).exists()
    assert Path(exports["markdown"]).exists()
    manifest = export_bundle_manifest(pack, exports)
    assert manifest["external_publish"] is False
    assert board_pack_safety_gate(pack.to_dict())["allowed"] is True
    assert board_pack_safety_gate(pack.to_dict(), external_publish_requested=True)["allowed"] is False
    assert board_pack_quality_check(pack.to_dict())["ok"] is True


def test_audit_control_ui_routes(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    audit = ReportingAuditLog(tmp_path / "reporting.db")
    event = audit.record("tester", "board_pack.test", "target")
    assert audit.list_events()[0]["id"] == event.id
    assert reporting_status()["ok"] is True
    demo = board_pack_demo(str(tmp_path))
    assert Path(demo["exports"]["json"]).exists()
    assert demo["safety"]["allowed"] is True
    assert reporting_overview()["status"]["ok"] is True
    assert "Enterprise Reporting and Board Pack" in render_board_overview_page()
    assert "KPIs" in render_kpis_page()
    assert "Decisions" in render_decisions_page()
    assert "Risks" in render_risks_page()
    assert route_board_pack_status()["ok"] is True
    assert route_board_pack_overview()["status"]["ok"] is True
    assert route_kpi_snapshot()["validation"]["ok"] is True
    assert route_board_registers()["validation"]["ok"] is True
    assert route_narrative_bundle()["safe_disclaimer"]
    assert Path(route_board_pack_demo()["exports"]["json"]).exists()
    assert "markdown" in route_board_pack_markdown()
    assert route_board_pack_safety()["safety"]["allowed"] is True
    assert "events" in route_reporting_audit()
    assert route_board_pack_page()["content_type"] == "text/html"
    assert route_board_kpis_page()["content_type"] == "text/html"
    assert route_board_decisions_page()["content_type"] == "text/html"
    assert route_board_risks_page()["content_type"] == "text/html"


def test_docs_scripts_assets_exist():
    root = Path(__file__).resolve().parents[1]
    for rel in [
        "scripts/board-pack/board-pack-status.sh",
        "scripts/board-pack/kpi-snapshot.sh",
        "scripts/board-pack/board-registers.sh",
        "scripts/board-pack/narrative-bundle.sh",
        "scripts/board-pack/board-pack-demo.sh",
        "scripts/board-pack/board-pack-markdown.sh",
        "scripts/board-pack/board-pack-safety.sh",
        "scripts/board-pack/reporting-audit.sh",
        "scripts/board-pack/board-dashboard-export.sh",
        "docs/board-pack/ENTERPRISE_REPORTING_BOARD_PACK_GUIDE.md",
        "docs/board-pack/KPI_SCORECARD.md",
        "docs/board-pack/BOARD_PACK_STRUCTURE.md",
        "docs/board-pack/DECISION_AND_RISK_REGISTER.md",
        "docs/board-pack/REPORTING_SAFETY_POLICY.md",
        "docs/requirements/NEXT_V32_ENTERPRISE_REPORTING_BOARD_PACK_REQUIREMENTS.md",
        "assets/board-pack/enterprise_reporting_board_pack_features.json",
    ]:
        assert (root / rel).exists(), rel
