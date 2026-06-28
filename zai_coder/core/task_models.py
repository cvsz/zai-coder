from __future__ import annotations

from dataclasses import dataclass
from typing import Any

TASK_SCHEMA_NAME = "task_queue"
TASK_SCHEMA_VERSION = 1

TASK_STATES: tuple[str, ...] = (
    "queued",
    "running",
    "waiting_approval",
    "completed",
    "failed",
    "cancelled",
)

TERMINAL_TASK_STATES = {"completed", "failed", "cancelled"}


def normalize_task_state(state: str) -> str:
    value = str(state or "").strip().lower()
    if value == "done":
        return "completed"
    if value == "canceled":
        return "cancelled"
    if value not in TASK_STATES:
        raise ValueError(f"Invalid task state: {state}")
    return value


def is_terminal_state(state: str) -> bool:
    return normalize_task_state(state) in TERMINAL_TASK_STATES


@dataclass(frozen=True)
class TaskRecord:
    id: int
    title: str
    agent: str
    prompt: str
    state: str
    status: str
    priority: int
    parent_id: int | None
    created_at: float
    updated_at: float
    started_at: float | None
    finished_at: float | None
    error: str | None
    attempt_count: int
    max_attempts: int
    lease_owner: str | None
    lease_expires_at: float | None

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "agent": self.agent,
            "prompt": self.prompt,
            "state": self.state,
            "status": self.status,
            "priority": self.priority,
            "parent_id": self.parent_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "error": self.error or "",
            "attempt_count": self.attempt_count,
            "max_attempts": self.max_attempts,
            "lease_owner": self.lease_owner or "",
            "lease_expires_at": self.lease_expires_at,
        }


@dataclass(frozen=True)
class TaskEventRecord:
    id: int
    task_id: int
    event_type: str
    message: str
    created_at: float

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "task_id": self.task_id,
            "event_type": self.event_type,
            "message": self.message,
            "created_at": self.created_at,
        }


@dataclass(frozen=True)
class TaskOutputRecord:
    id: int
    task_id: int
    role: str
    content: str
    created_at: float

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "task_id": self.task_id,
            "role": self.role,
            "content": self.content,
            "created_at": self.created_at,
        }

