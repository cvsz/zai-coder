"""Update manifest model for safe dry-run-first upgrades."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class UpdateManifest:
    version: str
    channel: str = "stable"
    files: List[str] = field(default_factory=list)
    checksums: Dict[str, str] = field(default_factory=dict)
    notes: str = ""
    requires_apply: bool = True

    def to_dict(self) -> dict:
        return {
            "version": self.version,
            "channel": self.channel,
            "files": list(self.files),
            "checksums": dict(self.checksums),
            "notes": self.notes,
            "requires_apply": self.requires_apply,
        }
