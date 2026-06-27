from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

from .task_store import TaskStore


class TaskQueue:
    def __init__(self, db_path: str | Path):
        self.store = TaskStore(db_path)

    def create(self, title: str, agent: str, prompt: str, *, priority: int = 100, parent_id: int | None = None, max_attempts: int = 3) -> dict[str, Any]:
        return self.store.create(title=title, agent=agent, prompt=prompt, priority=priority, parent_id=parent_id, max_attempts=max_attempts)

    def enqueue(self, title: str, agent: str, prompt: str, *, priority: int = 100, parent_id: int | None = None, max_attempts: int = 3) -> dict[str, Any]:
        return self.create(title, agent, prompt, priority=priority, parent_id=parent_id, max_attempts=max_attempts)

    def list_tasks(self) -> list[dict[str, Any]]:
        return self.store.list_tasks()

    def show(self, task_id: int) -> dict[str, Any] | None:
        return self.store.get_task(task_id)

    def update(self, task_id: int, state: str) -> dict[str, Any] | None:
        self.store.update_task_state(task_id, state)
        return self.show(task_id)

    def cancel(self, task_id: int) -> dict[str, Any] | None:
        return self.store.cancel_task(task_id)

    def retry(self, task_id: int) -> dict[str, Any] | None:
        return self.store.retry_task(task_id)

    def logs(self, task_id: int) -> list[dict[str, Any]]:
        return self.store.get_events(task_id)

    def outputs(self, task_id: int) -> list[dict[str, Any]]:
        return self.store.get_outputs(task_id)

    def export_json(self) -> dict[str, Any]:
        payload = self.store.export_json()
        payload["exported_at"] = time.time()
        return payload

    def export_json_text(self) -> str:
        return json.dumps(self.export_json(), indent=2, sort_keys=True)

    def lease_next(self, worker_id: str, lease_seconds: int = 300) -> dict[str, Any] | None:
        return self.store.claim_next_task(worker_id, lease_seconds=lease_seconds)

    def release_expired_leases(self) -> int:
        return self.store.release_expired_leases()

    def run_once(self, worker_id: str, apply: bool = True, lease_seconds: int = 300):
        from .task_runner import TaskRunner
        from .approvals import ActionApprover

        task = self.lease_next(worker_id, lease_seconds=lease_seconds)
        if task is None:
            return {"ok": True, "ran": False, "reason": "queue-empty"}
        runner = TaskRunner(self.store, ActionApprover(apply_mode=apply), worker_id=worker_id, lease_seconds=lease_seconds)
        result = runner.run(task["id"], apply=apply)
        return {"ok": True, "ran": True, "task": result or task}


class TaskQueueWorker:
    def __init__(self, queue: TaskQueue | None = None, *, worker_id: str = "local-worker", lease_seconds: int = 300):
        self.queue = queue or TaskQueue(Path(".zai-coder") / "tasks" / "tasks.db")
        self.worker_id = worker_id
        self.lease_seconds = lease_seconds

    def run_once(self, apply: bool = True) -> dict[str, Any]:
        return self.queue.run_once(self.worker_id, apply=apply, lease_seconds=self.lease_seconds)

    def drain(self, limit: int = 10, apply: bool = True) -> list[dict[str, Any]]:
        results: list[dict[str, Any]] = []
        for _ in range(max(0, limit)):
            result = self.run_once(apply=apply)
            results.append(result)
            if not result.get("ran"):
                break
        return results
