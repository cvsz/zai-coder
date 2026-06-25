"""Worker orchestration control plane helpers."""

from __future__ import annotations

from .registry import WorkerRegistry
from .queue import WorkerJobQueue
from .audit import WorkerAuditLog
from .tenant_guard import tenant_worker_guard
from .concurrency import concurrency_decision
from .retry_deadletter import retry_decision, dead_letter_payload
from .execution_bridge import execution_bridge_plan


def orchestrator_status() -> dict:
    return {
        "ok": True,
        "systems": [
            "worker_registry",
            "job_queue",
            "lease_heartbeat",
            "scheduler",
            "retry_policy",
            "dead_letter_queue",
            "concurrency_limits",
            "tenant_worker_guard",
            "execution_runner_bridge",
            "worker_audit_log",
        ],
    }


def lease_and_plan_next(queue: str = "maintenance", worker_name: str = "local-worker", db_path: str = "data/worker-orchestration.db") -> dict:
    registry = WorkerRegistry(db_path)
    jobs = WorkerJobQueue(db_path)
    audit = WorkerAuditLog(db_path)
    worker = registry.register(worker_name, queue)
    job = jobs.lease_next(queue, worker.id)
    if job is None:
        return {"ok": True, "leased": False, "worker": worker.to_dict(), "reason": "queue empty"}
    guard = tenant_worker_guard(worker.to_dict(), job.to_dict())
    if not guard["allowed"]:
        jobs.mark(job.id, "dead_letter")
        audit.record(worker.id, job.id, "tenant_denied", guard["reason"], guard)
        return {"ok": False, "leased": True, "worker": worker.to_dict(), "job": job.to_dict(), "guard": guard}
    concurrency = concurrency_decision(worker.to_dict(), running_jobs=0)
    if not concurrency["allowed"]:
        jobs.mark(job.id, "queued")
        return {"ok": False, "leased": False, "reason": "concurrency limit reached", "concurrency": concurrency}
    plan = execution_bridge_plan(job.to_dict())
    audit.record(worker.id, job.id, "planned", "execution bridge plan generated", plan)
    return {"ok": True, "leased": True, "worker": worker.to_dict(), "job": job.to_dict(), "plan": plan}


def fail_job_policy(job_dict: dict, error_type: str = "transient") -> dict:
    from .models import WorkerJob
    job = WorkerJob(**job_dict)
    decision = retry_decision(job, error_type)
    return {"decision": decision, "dead_letter": dead_letter_payload(job, decision["reason"]) if decision["action"] == "dead_letter" else None}
