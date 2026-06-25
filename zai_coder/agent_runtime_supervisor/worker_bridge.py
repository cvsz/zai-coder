"""Bridge agent tasks to worker orchestration jobs."""

from __future__ import annotations

from zai_coder.worker_orchestration.queue import WorkerJobQueue


def agent_task_worker_payload(task: dict) -> dict:
    return {
        "agent_id": task["agent_id"],
        "task_id": task["id"],
        "title": task["title"],
        "instruction": task["instruction"],
        "safe_mode": True,
    }


def worker_bridge_plan(task: dict, queue: str = "agents") -> dict:
    return {
        "dry_run": True,
        "queue": queue,
        "job_type": "agent_task",
        "org_id": task["org_id"],
        "workspace_id": task["workspace_id"],
        "payload": agent_task_worker_payload(task),
    }


def enqueue_agent_task_job(task: dict, queue: str = "agents", db_path: str = "data/worker-orchestration.db") -> dict:
    job = WorkerJobQueue(db_path).enqueue(
        queue,
        "agent_task",
        task["org_id"],
        task["workspace_id"],
        agent_task_worker_payload(task),
    )
    return job.to_dict()
