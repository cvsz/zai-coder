"""Board report section builder."""

from __future__ import annotations

from .models import ReportSection
from .narrative import narrative_bundle
from .kpis import kpi_scorecard, kpi_snapshot
from .decisions import board_action_summary


def board_sections(period: str = "Q1") -> list[dict]:
    narrative = narrative_bundle(period)
    scorecard = kpi_scorecard(kpi_snapshot())
    actions = board_action_summary()
    sections = [
        ReportSection("exec", "Executive Summary", narrative["executive_summary"], 10),
        ReportSection("investor", "Investor Update", narrative["investor_update"], 20),
        ReportSection("ops", "Operations Update", narrative["operations_update"], 30),
        ReportSection("compliance", "Compliance Update", narrative["compliance_update"], 40),
        ReportSection("kpis", "KPI Scorecard", str(scorecard), 50),
        ReportSection("decisions", "Board Decisions and Risks", str(actions), 60),
    ]
    reports = [{"id": section.id, "issues": section.validate()} for section in sections]
    if any(item["issues"] for item in reports):
        raise ValueError(str(reports))
    return [section.to_dict() for section in sorted(sections, key=lambda item: item.order)]
