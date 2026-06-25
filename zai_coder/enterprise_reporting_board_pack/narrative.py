"""Narrative generation for board reporting."""

from __future__ import annotations

from .kpis import kpi_scorecard, kpi_snapshot
from .decisions import board_action_summary


def executive_summary(period: str = "Q1") -> str:
    scorecard = kpi_scorecard(kpi_snapshot())
    actions = board_action_summary()
    return (
        f"For {period}, the ZAI Coder Control Plane advanced from platform hardening into enterprise reporting readiness. "
        f"The package now tracks {len(scorecard['scorecard'])} executive KPIs, with "
        f"{scorecard['counts']['green']} green indicators and {scorecard['counts']['yellow']} yellow indicators. "
        f"Board attention is requested for {len(actions['open_decisions'])} open decisions and "
        f"{len(actions['high_risks'])} high-risk items."
    )


def investor_update(period: str = "Q1") -> str:
    return (
        f"{period} investor update: the platform remains local-first, dry-run-first, and safety-gated. "
        "Core progress includes release automation, self-healing operations, compliance readiness, connector planning, "
        "and board-pack reporting. Current outputs are scaffold/readiness artifacts, not audited financial statements."
    )


def operations_update() -> str:
    return (
        "Operations update: worker orchestration, agent supervision, gateway routing, release center, and self-healing "
        "modules now expose plan-first workflows with audit logs and safety gates."
    )


def compliance_update() -> str:
    return (
        "Compliance update: the enterprise compliance center maps frameworks, controls, evidence, processing records, "
        "risk controls, attestations, and legal-hold guards. Outputs are readiness planning only and do not certify compliance."
    )


def narrative_bundle(period: str = "Q1") -> dict:
    return {
        "executive_summary": executive_summary(period),
        "investor_update": investor_update(period),
        "operations_update": operations_update(),
        "compliance_update": compliance_update(),
        "safe_disclaimer": "Reporting outputs are planning artifacts and must be reviewed before external use.",
    }
