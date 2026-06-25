"""Creative approval workflow."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


ALLOWED_TRANSITIONS = {
    "draft": {"review"},
    "review": {"approved", "draft"},
    "approved": {"active", "archived"},
    "active": {"archived"},
    "archived": set(),
}


@dataclass
class ApprovalEvent:
    from_status: str
    to_status: str
    actor: str
    note: str = ""
    created_at: str = field(default_factory=now_iso)

    def to_dict(self) -> dict:
        return {
            "from_status": self.from_status,
            "to_status": self.to_status,
            "actor": self.actor,
            "note": self.note,
            "created_at": self.created_at,
        }


def can_transition(from_status: str, to_status: str) -> bool:
    return to_status in ALLOWED_TRANSITIONS.get(from_status, set())


def transition_status(from_status: str, to_status: str, actor: str, note: str = "") -> ApprovalEvent:
    if not can_transition(from_status, to_status):
        raise ValueError(f"invalid transition: {from_status} -> {to_status}")
    return ApprovalEvent(from_status=from_status, to_status=to_status, actor=actor, note=note)
