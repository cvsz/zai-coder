from __future__ import annotations

import time

from zai_coder.core.task_queue import TaskQueue
from zai_coder.core.task_store import TaskStore


def test_task_store_schema_and_lifecycle(tmp_path):
    store = TaskStore(tmp_path / ".zai-coder" / "tasks" / "tasks.db")

    schema = store.schema_version()
    assert schema["name"] == "task_queue"
    assert schema["version"] == 1

    task_id = store.create_task("scan repo", "planner", "inspect the tree", priority=20, max_attempts=5)
    task = store.get_task(task_id)
    assert task is not None
    assert task["state"] == "queued"
    assert task["status"] == "queued"
    assert task["priority"] == 20
    assert task["attempt_count"] == 0
    assert task["max_attempts"] == 5

    store.add_event(task_id, "created", "Task created.")
    store.add_output(task_id, "assistant", "Working tree inspected.")
    assert store.get_events(task_id)[0]["message"] == "Task created."
    assert store.get_outputs(task_id)[0]["content"] == "Working tree inspected."

    store.update_task_state(task_id, "running")
    running = store.get_task(task_id)
    assert running["state"] == "running"
    assert running["started_at"] is not None

    store.update_task_state(task_id, "completed")
    completed = store.get_task(task_id)
    assert completed["state"] == "completed"
    assert completed["finished_at"] is not None

    exported = store.export_json()
    assert exported["schema_version"]["version"] == 1
    assert exported["tasks"][0]["id"] == task_id


def test_task_store_retry_and_lease_recovery(tmp_path):
    queue = TaskQueue(tmp_path / ".zai-coder" / "tasks" / "tasks.db")
    created = queue.create("draft plan", "planner", "draft a plan", priority=1)
    task_id = created["id"]

    leased = queue.lease_next("worker-1", lease_seconds=1)
    assert leased is not None
    assert leased["id"] == task_id
    assert leased["state"] == "running"
    assert leased["lease_owner"] == "worker-1"

    queue.store.update_task(task_id, lease_expires_at=time.time() - 10)
    assert queue.release_expired_leases() == 1
    assert queue.show(task_id)["state"] == "queued"

    queue.store.update_task_state(task_id, "failed", error="boom")
    retried = queue.retry(task_id)
    assert retried is not None
    assert retried["state"] == "queued"
    assert retried["error"] == ""

