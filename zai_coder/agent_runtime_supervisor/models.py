"""Agent Runtime Supervisor models.

The supervisor manages agent runtime metadata, lifecycle plans, permissions, and
worker-bridge plans. It is local-first and does not launch arbitrary processes.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class AgentRuntime:
    id: str
    name: str
    agent_type: str
    org_id: str
    workspace_id: str
    status: str = "stopped"
    model: str = "local/mock-agent"
    worker_queue: str = "agents"
    heartbeat_at: str = field(default_factory=now_iso)
    created_at: str = field(default_factory=now_iso)

    def validate(self) -> list[str]:
        issues: list[str] = []
        if not self.id or not self.name or not self.agent_type:
            issues.append("agent id, name, and agent_type required")
        if not self.org_id or not self.workspace_id:
            issues.append("agent requires org_id and workspace_id")
        if self.status not in {"stopped", "starting", "running", "paused", "crashed", "draining", "terminated"}:
            issues.append("invalid agent status")
        if "/" in self.worker_queue or ".." in self.worker_queue:
            issues.append("unsafe worker queue")
        return issues

    def to_dict(self) -> dict:
        return self.__dict__.copy()


@dataclass(frozen=True)
class AgentSandboxProfile:
    id: str
    name: str
    network_mode: str = "local-only"
    filesystem_mode: str = "workspace-scoped"
    max_runtime_seconds: int = 3600
    allowed_tools: tuple[str, ...] = ("read", "write-draft", "plan", "test")
    blocked_paths: tuple[str, ...] = (".env", "credentials.json", "apps/zlms/", ".git/")

    def validate(self) -> list[str]:
        issues: list[str] = []
        if self.network_mode not in {"local-only", "cloudflare-access", "offline"}:
            issues.append("invalid network_mode")
        if self.filesystem_mode not in {"read-only", "workspace-scoped", "ephemeral"}:
            issues.append("invalid filesystem_mode")
        if self.max_runtime_seconds <= 0:
            issues.append("max_runtime_seconds must be positive")
        return issues

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "network_mode": self.network_mode,
            "filesystem_mode": self.filesystem_mode,
            "max_runtime_seconds": self.max_runtime_seconds,
            "allowed_tools": list(self.allowed_tools),
            "blocked_paths": list(self.blocked_paths),
        }


@dataclass(frozen=True)
class AgentTask:
    id: str
    agent_id: str
    org_id: str
    workspace_id: str
    title: str
    instruction: str
    status: str = "queued"
    priority: int = 100
    created_at: str = field(default_factory=now_iso)

    def validate(self) -> list[str]:
        issues: list[str] = []
        if not self.id or not self.agent_id or not self.title:
            issues.append("task id, agent_id, and title required")
        if not self.org_id or not self.workspace_id:
            issues.append("task requires tenant context")
        if self.status not in {"queued", "assigned", "running", "completed", "failed", "cancelled"}:
            issues.append("invalid task status")
        if self.priority < 0:
            issues.append("priority must be >= 0")
        if len(self.instruction) > 20000:
            issues.append("instruction too large")
        return issues

    def to_dict(self) -> dict:
        return self.__dict__.copy()


@dataclass(frozen=True)
class AgentBudget:
    org_id: str
    workspace_id: str
    max_tasks_per_day: int = 100
    max_runtime_minutes_per_day: int = 240
    max_provider_apply_per_day: int = 10

    def validate(self) -> list[str]:
        issues: list[str] = []
        for key, value in self.__dict__.items():
            if key.startswith("max_") and value < 0:
                issues.append(f"{key} must be >= 0")
        return issues

    def to_dict(self) -> dict:
        return self.__dict__.copy()


@dataclass(frozen=True)
class AgentAuditEvent:
    id: str
    agent_id: str
    org_id: str
    workspace_id: str
    actor: str
    action: str
    target: str
    payload: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=now_iso)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "agent_id": self.agent_id,
            "org_id": self.org_id,
            "workspace_id": self.workspace_id,
            "actor": self.actor,
            "action": self.action,
            "target": self.target,
            "payload": dict(self.payload),
            "created_at": self.created_at,
        }
