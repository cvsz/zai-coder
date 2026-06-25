"""Draft delivery gates."""

from __future__ import annotations

from .channels import channel_policy


def delivery_gate(draft_payload: dict, approval_id: str = "", send_requested: bool = False) -> dict:
    policy = channel_policy(draft_payload["channel"])
    blocked = []
    if send_requested:
        blocked.append("actual sending is disabled by notification center")
    if draft_payload.get("status") != "draft" and not approval_id.startswith("approved_"):
        blocked.append("non-draft notification requires approval")
    if policy["external_delivery_disabled"]:
        blocked.append(f"external channel {draft_payload['channel']} is draft-only")
    if not draft_payload.get("dry_run", True):
        blocked.append("draft must remain dry-run")
    return {"allowed": not blocked, "blocked": blocked, "policy": policy, "draft_id": draft_payload.get("id")}


def digest_plan(drafts: list[dict], frequency: str = "daily") -> dict:
    if frequency not in {"daily", "weekly"}:
        raise ValueError("frequency must be daily or weekly")
    return {
        "dry_run": True,
        "frequency": frequency,
        "draft_count": len(drafts),
        "channels": sorted({draft["channel"] for draft in drafts}),
        "send": False,
        "requires_review": True,
    }
