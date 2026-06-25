"""Enterprise reporting and board pack control helpers."""

from __future__ import annotations

from pathlib import Path

from .kpis import kpi_snapshot, kpi_scorecard, kpi_validation_report
from .decisions import decision_register, risk_register, board_register_validation, board_action_summary
from .narrative import narrative_bundle
from .builder import build_board_pack, export_board_pack, export_bundle_manifest
from .validation import board_pack_safety_gate, board_pack_quality_check
from .audit import ReportingAuditLog


def reporting_status() -> dict:
    return {
        "ok": True,
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


def board_pack_demo(root: str = ".") -> dict:
    pack = build_board_pack("Q1")
    exports = export_board_pack(pack, root)
    manifest = export_bundle_manifest(pack, exports)
    safety = board_pack_safety_gate(pack.to_dict())
    quality = board_pack_quality_check(pack.to_dict())
    audit = ReportingAuditLog().record("system", "board_pack.generated", pack.id, manifest)
    return {"pack": pack.to_dict(), "exports": exports, "manifest": manifest, "safety": safety, "quality": quality, "audit": audit.to_dict()}


def reporting_overview() -> dict:
    return {
        "status": reporting_status(),
        "kpis": kpi_snapshot(),
        "scorecard": kpi_scorecard(),
        "kpi_validation": kpi_validation_report(),
        "decisions": decision_register(),
        "risks": risk_register(),
        "register_validation": board_register_validation(),
        "action_summary": board_action_summary(),
        "narrative": narrative_bundle("Q1"),
    }
