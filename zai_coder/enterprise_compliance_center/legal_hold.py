"""Retention and legal hold guard."""

from __future__ import annotations


def retention_delete_gate(record: dict, legal_hold: bool = False, approval_id: str = "") -> dict:
    blocked = []
    if legal_hold:
        blocked.append("legal hold active")
    if record.get("pii") and not approval_id.startswith("approved_"):
        blocked.append("PII retention deletion requires approval")
    if record.get("retention_days", 0) > 0:
        blocked.append("retention period not expired")
    return {"allowed": not blocked, "blocked": blocked, "record": record}


def legal_hold_policy() -> dict:
    return {
        "legal_hold_blocks_delete": True,
        "pii_delete_requires_approval": True,
        "audit_required": True,
        "export_redacts_secrets": True,
    }
