"""API key + role enforcement policy for production SaaS."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .permissions import has_permission


@dataclass(frozen=True)
class EnforcementDecision:
    allowed: bool
    reason: str
    actor: str = ""

    def to_dict(self) -> dict:
        return {"allowed": self.allowed, "reason": self.reason, "actor": self.actor}


def enforce_api_key(record, required_permission: str, roles: Iterable[str]) -> EnforcementDecision:
    if record is None:
        return EnforcementDecision(False, "missing-or-invalid-api-key")
    if not has_permission(roles, required_permission):
        return EnforcementDecision(False, "permission-denied", getattr(record, "name", "api-key"))
    return EnforcementDecision(True, "allowed", getattr(record, "name", "api-key"))
