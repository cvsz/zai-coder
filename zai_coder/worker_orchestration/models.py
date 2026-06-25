"""Worker orchestration models.

This module keeps worker orchestration local-first and tenant-aware. Workers do
not execute shell commands directly; execution can be bridged through the v18
approved execution runner.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class WorkerNode:
    id: str
    name: str
    queue: str
    tenant_scope: str = "shared"
    status: str = "idle"
    concurrency_limit: int = 1
    heartbeat_at: str = field(default_factory=now_iso)
    created_at: str = field(default_factory=now_iso)

    def validate(self) -> list[str]:
        issues: list[str] = []
        if not self.id or not self.name or not self.queue:
            issues.append("worker id, name, and queue required")
        if self.status not in {"idle", "busy", "draining", "offline", "failed"}:
            issues.append("invalid worker status")
        if self.concurrency_limit < 1:
            issues.append("concurrency_limit must be >= 1")
        if "/" in self.queue or ".." in self.queue:
            issues.append("unsafe queue name")
        return issues

    def to_dict(self) -> dict:
        return self.__dict__.copy()


@dataclass(frozen=True)
class WorkerJob:
    id: str
    queue: str
    job_type: str
    org_id: str
    workspace_id: str
    payload: dict[str, Any] = field(default_factory=dict)
    status: str = "queued"
    priority: int = 100
    attempts: int = 0
    max_attempts: int = 3
    lease_worker_id: str = ""
    lease_expires_at: str = ""
    created_at: str = field(default_factory=now_iso)

    def validate(self) -> list[str]:
        issues: list[str] = []
        if not self.id or not self.queue or not self.job_type:
            issues.append("job id, queue, and job_type required")
        if not self.org_id or not self.workspace_id:
            issues.append("job requires org_id and workspace_id")
        if self.status not in {"queued", "leased", "running", "completed", "failed", "dead_letter", "cancelled"}:
            issues.append("invalid job status")
        if self.priority < 0:
            issues.append("priority must be >= 0")
        if self.max_attempts < 1:
            issues.append("max_attempts must be >= 1")
        return issues

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "queue": self.queue,
            "job_type": self.job_type,
            "org_id": self.org_id,
            "workspace_id": self.workspace_id,
            "payload": dict(self.payload),
            "status": self.status,
            "priority": self.priority,
            "attempts": self.attempts,
            "max_attempts": self.max_attempts,
            "lease_worker_id": self.lease_worker_id,
            "lease_expires_at": self.lease_expires_at,
            "created_at": self.created_at,
        }


@dataclass(frozen=True)
class WorkerSchedule:
    id: str
    name: str
    queue: str
    job_type: str
    cron: str
    enabled: bool = True
    payload: dict[str, Any] = field(default_factory=dict)

    def validate(self) -> list[str]:
        issues = []
        if not self.id or not self.name:
            issues.append("schedule id/name required")
        if not self.queue or not self.job_type:
            issues.append("schedule queue/job_type required")
        if len(self.cron.split()) != 5:
            issues.append("cron must have 5 fields")
        return issues

    def to_dict(self) -> dict:
        return {"id": self.id, "name": self.name, "queue": self.queue, "job_type": self.job_type, "cron": self.cron, "enabled": self.enabled, "payload": dict(self.payload)}


@dataclass(frozen=True)
class WorkerEvent:
    id: str
    worker_id: str
    job_id: str
    event_type: str
    message: str
    payload: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=now_iso)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "worker_id": self.worker_id,
            "job_id": self.job_id,
            "event_type": self.event_type,
            "message": self.message,
            "payload": dict(self.payload),
            "created_at": self.created_at,
        }
