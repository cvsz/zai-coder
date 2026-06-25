"""Shared models for integration adapters."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass(frozen=True)
class IntegrationPlan:
    provider: str
    action: str
    dry_run: bool = True
    commands: List[str] = field(default_factory=list)
    files: Dict[str, str] = field(default_factory=dict)
    payload: Dict[str, object] = field(default_factory=dict)
    warnings: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "provider": self.provider,
            "action": self.action,
            "dry_run": self.dry_run,
            "commands": list(self.commands),
            "files": dict(self.files),
            "payload": dict(self.payload),
            "warnings": list(self.warnings),
        }


def ensure_dry_run(plan: IntegrationPlan) -> IntegrationPlan:
    if not plan.dry_run:
        raise ValueError("integration plans must be dry-run by default")
    return plan
