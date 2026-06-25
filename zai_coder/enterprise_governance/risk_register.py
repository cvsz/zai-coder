"""Risk register."""

from __future__ import annotations

from .models import RiskItem


DEFAULT_RISKS = [
    RiskItem("risk-001", "Public admin exposure without Access", "security", 3, 5, "Require Cloudflare Access before DNS route."),
    RiskItem("risk-002", "Secret committed to repo", "security", 2, 5, "Run secret scan and block .env patterns."),
    RiskItem("risk-003", "Migration without backup", "operations", 3, 4, "Require backup before migrations."),
    RiskItem("risk-004", "Provider operation applied without approval", "governance", 2, 5, "Approval guard and audit log."),
]


def risk_register() -> list[dict]:
    return [risk.to_dict() for risk in DEFAULT_RISKS]


def risk_summary() -> dict:
    risks = DEFAULT_RISKS
    high = [r for r in risks if r.score >= 12 and r.status != "closed"]
    return {"ok": not any(r.score >= 20 for r in risks), "total": len(risks), "high_or_above": len(high), "risks": [r.to_dict() for r in risks]}
