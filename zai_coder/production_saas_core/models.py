"""Production SaaS core data models."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class Organization:
    id: str
    slug: str
    name: str
    owner_user_id: str
    plan_slug: str = "free"
    status: str = "active"
    created_at: str = field(default_factory=now_iso)

    def validate(self) -> list[str]:
        issues = []
        if not self.id:
            issues.append("missing id")
        if not self.slug:
            issues.append("missing slug")
        if not self.name:
            issues.append("missing name")
        if not self.owner_user_id:
            issues.append("missing owner_user_id")
        if self.status not in {"active", "suspended", "archived"}:
            issues.append(f"invalid status: {self.status}")
        return issues

    def to_dict(self) -> dict:
        return self.__dict__.copy()


@dataclass
class Workspace:
    id: str
    org_id: str
    slug: str
    name: str
    status: str = "active"
    created_at: str = field(default_factory=now_iso)

    def validate(self) -> list[str]:
        issues = []
        if not self.id:
            issues.append("missing id")
        if not self.org_id:
            issues.append("missing org_id")
        if not self.slug:
            issues.append("missing slug")
        if not self.name:
            issues.append("missing name")
        if self.status not in {"active", "archived"}:
            issues.append(f"invalid status: {self.status}")
        return issues

    def to_dict(self) -> dict:
        return self.__dict__.copy()


@dataclass
class UserAccount:
    id: str
    email: str
    display_name: str
    status: str = "active"
    created_at: str = field(default_factory=now_iso)

    def validate(self) -> list[str]:
        issues = []
        if not self.id:
            issues.append("missing id")
        if "@" not in self.email:
            issues.append("email must be valid")
        if not self.display_name:
            issues.append("missing display_name")
        if self.status not in {"active", "disabled", "invited"}:
            issues.append(f"invalid status: {self.status}")
        return issues

    def to_dict(self) -> dict:
        return self.__dict__.copy()


@dataclass
class Invitation:
    id: str
    org_id: str
    email: str
    role: str
    invited_by_user_id: str
    status: str = "pending"
    created_at: str = field(default_factory=now_iso)

    def validate(self) -> list[str]:
        issues = []
        if not self.org_id:
            issues.append("missing org_id")
        if "@" not in self.email:
            issues.append("email must be valid")
        if self.role not in {"owner", "admin", "developer", "marketer", "viewer", "billing"}:
            issues.append(f"invalid role: {self.role}")
        if self.status not in {"pending", "accepted", "revoked", "expired"}:
            issues.append(f"invalid status: {self.status}")
        return issues

    def to_dict(self) -> dict:
        return self.__dict__.copy()
