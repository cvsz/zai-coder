"""Board decision and risk registers."""

from __future__ import annotations

from .models import BoardDecision, BoardRisk


DEFAULT_DECISIONS = [
    BoardDecision("bd-release", "Approve v32 reporting package direction", "Founder", "proposed", "strategic", context="Continue enterprise-grade control-plane packaging."),
    BoardDecision("bd-compliance", "Prioritize SOC 2 evidence completion", "Compliance Owner", "proposed", "compliance", context="Evidence gaps remain for non-access controls."),
    BoardDecision("bd-connectors", "Select next production connector target", "Platform Owner", "deferred", "product", context="Connector hub currently contains plan-only adapters."),
]

DEFAULT_RISKS = [
    BoardRisk("br-certification", "Compliance readiness could be mistaken for certification", "medium", "Compliance Owner", "Label all outputs as readiness planning only."),
    BoardRisk("br-provider", "Provider adapters are plan-only and not production integrated", "medium", "Platform Owner", "Keep connector status explicit and gate real provider apply flows."),
    BoardRisk("br-operational", "Auto-healing must not execute destructive remediation", "high", "Ops Owner", "Require dry-run, rollback, approval, and approved execution runner."),
]


def decision_register() -> list[dict]:
    return [decision.to_dict() for decision in DEFAULT_DECISIONS]


def risk_register() -> list[dict]:
    return [risk.to_dict() for risk in DEFAULT_RISKS]


def board_register_validation() -> dict:
    decision_reports = [{"id": item.id, "issues": item.validate()} for item in DEFAULT_DECISIONS]
    risk_reports = [{"id": item.id, "issues": item.validate()} for item in DEFAULT_RISKS]
    return {
        "ok": all(not item["issues"] for item in decision_reports + risk_reports),
        "decisions": decision_reports,
        "risks": risk_reports,
    }


def board_action_summary() -> dict:
    decisions = decision_register()
    risks = risk_register()
    return {
        "open_decisions": [d for d in decisions if d["status"] in {"proposed", "deferred"}],
        "high_risks": [r for r in risks if r["severity"] in {"high", "critical"} and r["status"] != "closed"],
        "counts": {
            "decisions": len(decisions),
            "risks": len(risks),
            "high_risks": sum(1 for r in risks if r["severity"] in {"high", "critical"}),
        },
    }
