from __future__ import annotations

from typing import Any

from .approvals import ActionApprover
from .task_models import is_terminal_state
from .task_store import TaskStore


class TaskRunner:
    def __init__(self, store: TaskStore, approver: ActionApprover, *, worker_id: str = "task-runner", lease_seconds: int = 300):
        self.store = store
        self.approver = approver
        self.worker_id = worker_id
        self.lease_seconds = lease_seconds

    def run(self, task_id: int, apply: bool | None = None) -> dict[str, Any] | None:
        task_data = self.store.get_task(task_id)
        if not task_data:
            print(f"Task {task_id} not found.")
            return None

        if is_terminal_state(task_data["state"]):
            print(f"Task {task_id} already finished.")
            return task_data

        apply_mode = self.approver.apply_mode if apply is None else apply
        if not apply_mode:
            self.store.add_event(task_id, "dry-run", "Task execution skipped in dry-run mode.")
            self.store.update_task_state(task_id, "cancelled")
            self.store.add_output(task_id, "system", "Dry run completed without execution.")
            print(f"Task {task_id} cancelled.")
            return self.store.get_task(task_id)

        print(f"Starting task {task_id}: {task_data['title']}")
        if task_data["state"] == "queued":
            self.store.update_task(
                task_id,
                state="running",
                attempt_count=task_data["attempt_count"] + 1,
                lease_owner=self.worker_id,
                lease_expires_at=None,
            )
        else:
            self.store.update_task(
                task_id,
                state="running",
                lease_owner=self.worker_id,
                lease_expires_at=None,
            )
        self.store.add_event(task_id, "start", "Task execution started.")

        try:
            if not self.approver.check("run_command", f"Execute task '{task_data['title']}'"):
                self.store.update_task_state(task_id, "cancelled")
                self.store.add_event(task_id, "cancel", "Task cancelled by user.")
                print(f"Task {task_id} cancelled.")
                return self.store.get_task(task_id)

            self.store.update_task_state(task_id, "completed")
            self.store.add_event(task_id, "complete", "Task finished successfully.")
            self.store.add_output(task_id, "assistant", "Done.")
            print(f"Task {task_id} completed successfully.")
            return self.store.get_task(task_id)

        except Exception as exc:  # pragma: no cover - defensive execution guard
            self.store.update_task_state(task_id, "failed", error=str(exc))
            self.store.add_event(task_id, "fail", f"Task failed: {exc}")
            print(f"Task {task_id} failed: {exc}")
            return self.store.get_task(task_id)
