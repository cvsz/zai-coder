"""Execution runner models."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class CommandSpec:
    command: tuple[str, ...]
    cwd: str = "."
    timeout_seconds: int = 60
    env_overlay: dict[str, str] = field(default_factory=dict)
    apply: bool = False
    approval_id: str = ""

    def to_dict(self) -> dict:
        return {
            "command": list(self.command),
            "cwd": self.cwd,
            "timeout_seconds": self.timeout_seconds,
            "env_keys": sorted(self.env_overlay.keys()),
            "apply": self.apply,
            "approval_id": self.approval_id,
        }


@dataclass(frozen=True)
class QueueItem:
    id: str
    provider: str
    action: str
    command: CommandSpec
    status: str = "queued"
    attempts: int = 0
    created_at: str = field(default_factory=now_iso)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "provider": self.provider,
            "action": self.action,
            "command": self.command.to_dict(),
            "status": self.status,
            "attempts": self.attempts,
            "created_at": self.created_at,
        }


@dataclass(frozen=True)
class ExecutionResult:
    id: str
    ok: bool
    status: str
    returncode: int | None
    stdout: str
    stderr: str
    dry_run: bool
    started_at: str
    finished_at: str
    blocked_reasons: tuple[str, ...] = ()

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "ok": self.ok,
            "status": self.status,
            "returncode": self.returncode,
            "stdout": self.stdout,
            "stderr": self.stderr,
            "dry_run": self.dry_run,
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "blocked_reasons": list(self.blocked_reasons),
        }
