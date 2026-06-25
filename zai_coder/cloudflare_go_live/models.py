"""Cloudflare go-live models."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
import re


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


HOSTNAME_RE = re.compile(r"^(?=.{1,253}$)(?!-)[A-Za-z0-9-]{1,63}(?<!-)(\.(?!-)[A-Za-z0-9-]{1,63}(?<!-))+$")


@dataclass(frozen=True)
class CloudflareGoLiveConfig:
    hostname: str = "zai.example.com"
    local_service_url: str = "http://127.0.0.1:8765"
    tunnel_name: str = "zai-coder-control-plane"
    access_app_name: str = "ZAI Coder Control Plane"
    zone_name: str = "example.com"
    allow_emails: tuple[str, ...] = ()
    block_public_without_access: bool = True

    def validate(self) -> list[str]:
        issues: list[str] = []
        if not HOSTNAME_RE.match(self.hostname):
            issues.append("hostname must be a DNS hostname")
        if not self.local_service_url.startswith("http://127.0.0.1:") and not self.local_service_url.startswith("http://localhost:"):
            issues.append("local_service_url must be localhost-first")
        if not self.tunnel_name:
            issues.append("tunnel_name required")
        if not self.zone_name or "." not in self.zone_name:
            issues.append("zone_name must be a DNS zone")
        return issues

    def to_dict(self) -> dict:
        return {
            "hostname": self.hostname,
            "local_service_url": self.local_service_url,
            "tunnel_name": self.tunnel_name,
            "access_app_name": self.access_app_name,
            "zone_name": self.zone_name,
            "allow_emails": list(self.allow_emails),
            "block_public_without_access": self.block_public_without_access,
        }


@dataclass(frozen=True)
class GoLivePlan:
    name: str
    steps: tuple[str, ...]
    commands: tuple[str, ...] = ()
    files: dict[str, str] = field(default_factory=dict)
    dry_run: bool = True
    warnings: tuple[str, ...] = ()

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "steps": list(self.steps),
            "commands": list(self.commands),
            "files": dict(self.files),
            "dry_run": self.dry_run,
            "warnings": list(self.warnings),
        }
