"""Data models for local members and team workspaces."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class Member:
    id: str
    email: str
    display_name: str
    roles: List[str] = field(default_factory=lambda: ["viewer"])
    status: str = "active"
    created_at: str = field(default_factory=now_iso)
    updated_at: str = field(default_factory=now_iso)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "email": self.email,
            "display_name": self.display_name,
            "roles": list(self.roles),
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


@dataclass
class Invite:
    id: str
    email: str
    roles: List[str]
    invited_by: str
    status: str = "pending"
    created_at: str = field(default_factory=now_iso)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "email": self.email,
            "roles": list(self.roles),
            "invited_by": self.invited_by,
            "status": self.status,
            "created_at": self.created_at,
        }
