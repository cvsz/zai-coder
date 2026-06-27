from __future__ import annotations

from zai_coder.core.approvals import ActionApprover
from zai_coder.core.task_queue import TaskQueue, TaskQueueWorker
from zai_coder.core.task_runner import TaskRunner


def test_queue_worker_runs_and_completes_task(tmp_path, monkeypatch):
    queue = TaskQueue(tmp_path / ".zai-coder" / "tasks" / "tasks.db")
    task = queue.create("run diagnostics", "planner", "inspect repository")

    monkeypatch.setattr("zai_coder.core.approvals.prompt_for_approval", lambda _: True)

    worker = TaskQueueWorker(queue=queue, worker_id="worker-1", lease_seconds=60)
    result = worker.run_once(apply=True)

    assert result["ok"] is True
    assert result["ran"] is True
    assert result["task"]["id"] == task["id"]
    assert result["task"]["state"] == "completed"
    assert queue.show(task["id"])["finished_at"] is not None


def test_runner_dry_run_cancels_task(tmp_path):
    queue = TaskQueue(tmp_path / ".zai-coder" / "tasks" / "tasks.db")
    task = queue.create("simulate task", "planner", "dry run only")

    runner = TaskRunner(queue.store, ActionApprover(apply_mode=False))
    result = runner.run(task["id"], apply=False)

    assert result["state"] == "cancelled"
    assert queue.show(task["id"])["state"] == "cancelled"

