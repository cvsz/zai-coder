"""Content approval workflow."""

from __future__ import annotations

import uuid

from .models import ContentApproval


def create_approval(content_id: str, reviewer: str = "owner") -> ContentApproval:
    approval = ContentApproval(f"cap_{uuid.uuid4().hex[:12]}", content_id, "pending", reviewer)
    issues = approval.validate()
    if issues:
        raise ValueError("; ".join(issues))
    return approval


def approval_decision(approval_payload: dict, status: str, reviewer: str, notes: str = "") -> dict:
    approval = ContentApproval(
        id=approval_payload["id"],
        content_id=approval_payload["content_id"],
        status=status,
        reviewer=reviewer,
        notes=notes,
    )
    issues = approval.validate()
    return {
        "dry_run": True,
        "allowed": not issues,
        "issues": issues,
        "approval": approval.to_dict(),
        "publish": False,
    }


def approval_policy() -> dict:
    return {
        "approval_required_before_external_use": True,
        "publish_disabled": True,
        "reviewer_required": True,
        "audit_required": True,
    }
