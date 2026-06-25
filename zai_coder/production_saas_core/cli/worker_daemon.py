"""Worker daemon command facade."""

from __future__ import annotations

from pathlib import Path

from zai_coder.app_studio.worker import WorkerQueue


def worker_run_once(db_path: str | Path = "data/zai-worker.db") -> dict:
    queue = WorkerQueue(db_path)
    queue.register_handler("noop", lambda payload: {"ok": True, "payload": payload})
    job = queue.run_one()
    if job is None:
        return {"ran": False, "reason": "no queued job"}
    return {"ran": True, "job": job.to_dict()}
