"""Change approval workflow."""

from __future__ import annotations

from .models import ChangeRequest


REQUIRED_APPROVALS = {"low": 1, "medium": 1, "high": 2, "critical": 2}


def approval_requirement(risk_level: str) -> int:
    if risk_level not in REQUIRED_APPROVALS:
        raise ValueError("invalid risk level")
    return REQUIRED_APPROVALS[risk_level]


def change_approval_decision(change: ChangeRequest) -> dict:
    issues = change.validate()
    if issues:
        return {"allowed": False, "reason": "; ".join(issues), "required_approvals": 0, "current_approvals": len(change.approvals)}
    required = approval_requirement(change.risk_level)
    allowed = len(set(change.approvals)) >= required
    return {
        "allowed": allowed,
        "reason": "approval threshold met" if allowed else "more approvals required",
        "required_approvals": required,
        "current_approvals": len(set(change.approvals)),
        "change": change.to_dict(),
    }


def sample_change_request() -> ChangeRequest:
    return ChangeRequest(
        id="chg-001",
        title="Cloudflare go-live",
        requester="local-operator",
        risk_level="high",
        target="zai.example.com",
        approvals=("platform-owner",),
    )
