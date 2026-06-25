"""Enterprise Reporting and Board Pack route registry."""

from __future__ import annotations

from zai_coder.enterprise_reporting_board_pack.control import reporting_status, reporting_overview, board_pack_demo
from zai_coder.enterprise_reporting_board_pack.kpis import kpi_snapshot, kpi_scorecard, kpi_validation_report
from zai_coder.enterprise_reporting_board_pack.decisions import decision_register, risk_register, board_register_validation, board_action_summary
from zai_coder.enterprise_reporting_board_pack.narrative import narrative_bundle
from zai_coder.enterprise_reporting_board_pack.builder import build_board_pack, board_pack_markdown
from zai_coder.enterprise_reporting_board_pack.validation import board_pack_safety_gate, board_pack_quality_check
from zai_coder.enterprise_reporting_board_pack.audit import ReportingAuditLog
from zai_coder.enterprise_reporting_board_pack.ui.pages import render_board_overview_page, render_kpis_page, render_decisions_page, render_risks_page


def route_board_pack_status() -> dict:
    return {
        "ok": True,
        "service": "zai-enterprise-reporting-board-pack",
        "systems": [
            "executive_kpi_snapshot",
            "board_report_generator",
            "investor_update_summary",
            "operations_summary",
            "compliance_summary",
            "quarterly_pack_builder",
            "export_bundle_manifest",
            "risk_decision_register",
            "reporting_dashboard",
            "reporting_audit_log",
        ],
    }


def route_board_pack_overview() -> dict:
    return reporting_overview()


def route_kpi_snapshot() -> dict:
    return {"kpis": kpi_snapshot(), "scorecard": kpi_scorecard(), "validation": kpi_validation_report()}


def route_board_registers() -> dict:
    return {"decisions": decision_register(), "risks": risk_register(), "validation": board_register_validation(), "summary": board_action_summary()}


def route_narrative_bundle() -> dict:
    return narrative_bundle("Q1")


def route_board_pack_demo() -> dict:
    return board_pack_demo(".")


def route_board_pack_markdown() -> dict:
    pack = build_board_pack("Q1")
    return {"markdown": board_pack_markdown(pack), "pack": pack.to_dict()}


def route_board_pack_safety() -> dict:
    pack = build_board_pack("Q1").to_dict()
    return {"safety": board_pack_safety_gate(pack), "quality": board_pack_quality_check(pack)}


def route_reporting_audit() -> dict:
    return {"events": ReportingAuditLog().list_events()}


def route_board_pack_page() -> dict:
    return {"content_type": "text/html", "html": render_board_overview_page()}


def route_board_kpis_page() -> dict:
    return {"content_type": "text/html", "html": render_kpis_page()}


def route_board_decisions_page() -> dict:
    return {"content_type": "text/html", "html": render_decisions_page()}


def route_board_risks_page() -> dict:
    return {"content_type": "text/html", "html": render_risks_page()}
