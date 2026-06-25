"""Worker concurrency policy."""

from __future__ import annotations


def concurrency_decision(worker: dict, running_jobs: int) -> dict:
    limit = int(worker.get("concurrency_limit", 1))
    if running_jobs < 0:
        raise ValueError("running_jobs must be >= 0")
    allowed = running_jobs < limit
    return {"allowed": allowed, "running_jobs": running_jobs, "limit": limit, "remaining": max(limit - running_jobs, 0)}


def queue_concurrency_policy() -> dict:
    return {
        "default_limit": 1,
        "max_limit": 10,
        "tenant_scoped": True,
        "rules": [
            "worker cannot exceed its concurrency_limit",
            "tenant-scoped workers only process matching tenant jobs",
            "shared workers must pass tenant guard before execution",
        ],
    }
