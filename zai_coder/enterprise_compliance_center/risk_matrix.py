"""Risk and control matrix."""

from __future__ import annotations


def risk_score(likelihood: int, impact: int) -> int:
    if not (1 <= likelihood <= 5 and 1 <= impact <= 5):
        raise ValueError("likelihood and impact must be 1..5")
    return likelihood * impact


def risk_level(score: int) -> str:
    if score >= 20:
        return "critical"
    if score >= 12:
        return "high"
    if score >= 6:
        return "medium"
    return "low"


def risk_control_matrix() -> list[dict]:
    rows = [
        {"risk_id": "risk-access", "title": "Unauthorized cross-tenant access", "likelihood": 2, "impact": 5, "controls": ["cc-access-001"]},
        {"risk_id": "risk-audit-gap", "title": "Missing audit evidence", "likelihood": 3, "impact": 4, "controls": ["cc-audit-001"]},
        {"risk_id": "risk-data-retention", "title": "Incorrect data retention", "likelihood": 2, "impact": 4, "controls": ["gdpr-data-001"]},
    ]
    for row in rows:
        score = risk_score(row["likelihood"], row["impact"])
        row["score"] = score
        row["level"] = risk_level(score)
    return rows


def risk_acceptance_gate(row: dict, approval_id: str = "") -> dict:
    if row["level"] in {"high", "critical"} and not approval_id.startswith("approved_"):
        return {"allowed": False, "reason": "high/critical risk acceptance requires approval", "risk": row}
    return {"allowed": True, "reason": "risk acceptance gate passed", "risk": row}
