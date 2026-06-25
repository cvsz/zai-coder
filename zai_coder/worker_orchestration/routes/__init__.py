"""Worker orchestration route registry."""

from __future__ import annotations

from zai_coder.worker_orchestration.registry import WorkerRegistry
from zai_coder.worker_orchestration.queue import WorkerJobQueue
from zai_coder.worker_orchestration.scheduler import schedule_manifest, schedule_fire_plan
from zai_coder.worker_orchestration.concurrency import queue_concurrency_policy
from zai_coder.worker_orchestration.tenant_guard import tenant_worker_guard
from zai_coder.worker_orchestration.execution_bridge import execution_bridge_plan
from zai_coder.worker_orchestration.audit import WorkerAuditLog
from zai_coder.worker_orchestration.control import orchestrator_status, lease_and_plan_next, fail_job_policy
from zai_coder.worker_orchestration.ui.pages import render_worker_overview, render_schedules_page, render_worker_policy_page


def route_worker_status() -> dict:
    return {
        "ok": True,
        "service": "zai-worker-orchestration",
        "systems": [
            "worker_registry",
            "job_queue",
            "lease_heartbeat",
            "scheduler",
            "retry_dead_letter_policy",
            "concurrency_limits",
            "tenant_scoped_worker_guard",
            "execution_runner_bridge",
            "worker_dashboard",
            "worker_audit_log",
        ],
    }


def route_worker_register_demo() -> dict:
    worker = WorkerRegistry().register("local-worker", "maintenance")
    return worker.to_dict()


def route_worker_enqueue_demo() -> dict:
    job = WorkerJobQueue().enqueue("maintenance", "health_snapshot", "org_local", "ws_default", {"source": "demo"})
    return job.to_dict()


def route_worker_lease_demo() -> dict:
    queue = WorkerJobQueue()
    registry = WorkerRegistry()
    worker = registry.register("local-worker", "maintenance")
    job = queue.enqueue("maintenance", "health_snapshot", "org_local", "ws_default")
    leased = queue.lease_next("maintenance", worker.id)
    return {"worker": worker.to_dict(), "job": job.to_dict(), "leased": leased.to_dict() if leased else None}


def route_worker_schedules() -> dict:
    return {"schedules": schedule_manifest()}


def route_worker_schedule_fire(schedule_id: str = "sched_health") -> dict:
    return schedule_fire_plan(schedule_id)


def route_worker_policy() -> dict:
    return queue_concurrency_policy()


def route_worker_tenant_guard() -> dict:
    return tenant_worker_guard(
        {"tenant_scope": "org_local:ws_default"},
        {"org_id": "org_local", "workspace_id": "ws_default"},
    )


def route_worker_execution_bridge() -> dict:
    job = {"id": "job_demo", "job_type": "health_snapshot"}
    return execution_bridge_plan(job)


def route_worker_lease_and_plan() -> dict:
    queue = WorkerJobQueue()
    queue.enqueue("maintenance", "health_snapshot", "org_local", "ws_default")
    return lease_and_plan_next("maintenance")


def route_worker_fail_policy() -> dict:
    job = WorkerJobQueue().enqueue("maintenance", "health_snapshot", "org_local", "ws_default")
    return fail_job_policy(job.to_dict(), "transient")


def route_worker_audit() -> dict:
    return {"events": WorkerAuditLog().list_events()}


def route_worker_page() -> dict:
    return {"content_type": "text/html", "html": render_worker_overview()}


def route_worker_schedules_page() -> dict:
    return {"content_type": "text/html", "html": render_schedules_page()}


def route_worker_policy_page() -> dict:
    return {"content_type": "text/html", "html": render_worker_policy_page()}
