from pathlib import Path
import tempfile

from zai_coder.worker_orchestration.models import WorkerNode, WorkerJob, WorkerSchedule
from zai_coder.worker_orchestration.registry import WorkerRegistry
from zai_coder.worker_orchestration.queue import WorkerJobQueue
from zai_coder.worker_orchestration.retry_deadletter import retry_decision, dead_letter_payload
from zai_coder.worker_orchestration.concurrency import concurrency_decision, queue_concurrency_policy
from zai_coder.worker_orchestration.tenant_guard import tenant_worker_guard, tenant_worker_scope
from zai_coder.worker_orchestration.scheduler import schedule_manifest, schedule_fire_plan
from zai_coder.worker_orchestration.execution_bridge import job_to_command, execution_bridge_plan
from zai_coder.worker_orchestration.audit import WorkerAuditLog
from zai_coder.worker_orchestration.control import orchestrator_status, lease_and_plan_next, fail_job_policy
from zai_coder.worker_orchestration.ui.pages import render_worker_overview, render_schedules_page, render_worker_policy_page
from zai_coder.worker_orchestration.routes import (
    route_worker_status,
    route_worker_register_demo,
    route_worker_enqueue_demo,
    route_worker_lease_demo,
    route_worker_schedules,
    route_worker_schedule_fire,
    route_worker_policy,
    route_worker_tenant_guard,
    route_worker_execution_bridge,
    route_worker_lease_and_plan,
    route_worker_fail_policy,
    route_worker_audit,
    route_worker_page,
    route_worker_schedules_page,
    route_worker_policy_page,
)


def test_models_validation():
    assert WorkerNode("w", "Worker", "q").validate() == []
    assert WorkerNode("", "", "../bad", status="bad", concurrency_limit=0).validate()
    assert WorkerJob("j", "q", "health_snapshot", "org", "ws").validate() == []
    assert WorkerJob("", "", "", "", "", status="bad", max_attempts=0).validate()
    assert WorkerSchedule("s", "Schedule", "q", "job", "*/5 * * * *").validate() == []
    assert WorkerSchedule("", "", "", "", "* *").validate()


def test_registry_queue_lease_audit():
    with tempfile.TemporaryDirectory() as td:
        db = Path(td) / "workers.db"
        registry = WorkerRegistry(db)
        queue = WorkerJobQueue(db)
        audit = WorkerAuditLog(db)
        worker = registry.register("local-worker", "maintenance", concurrency_limit=2)
        assert registry.heartbeat(worker.id, "busy").status == "busy"
        assert registry.list_workers("maintenance")
        job = queue.enqueue("maintenance", "health_snapshot", "org", "ws", {"demo": True}, priority=1)
        leased = queue.lease_next("maintenance", worker.id)
        assert leased.id == job.id
        assert leased.status == "leased"
        queue.mark(job.id, "completed")
        assert queue.list_jobs("completed")[0]["id"] == job.id
        event = audit.record(worker.id, job.id, "completed", "job completed")
        assert audit.list_events()[0]["id"] == event.id


def test_retry_concurrency_tenant_guard():
    job = WorkerJob("j", "q", "health_snapshot", "org", "ws", attempts=1, max_attempts=3)
    assert retry_decision(job)["retry"] is True
    maxed = WorkerJob("j", "q", "health_snapshot", "org", "ws", attempts=3, max_attempts=3)
    assert retry_decision(maxed)["action"] == "dead_letter"
    assert dead_letter_payload(maxed, "done")["status"] == "dead_letter"
    assert concurrency_decision({"concurrency_limit": 2}, 1)["allowed"] is True
    assert concurrency_decision({"concurrency_limit": 2}, 2)["allowed"] is False
    assert queue_concurrency_policy()["tenant_scoped"] is True
    assert tenant_worker_scope("org", "ws") == "org:ws"
    assert tenant_worker_guard({"tenant_scope":"org:ws"}, {"org_id":"org","workspace_id":"ws"})["allowed"] is True
    assert tenant_worker_guard({"tenant_scope":"org:other"}, {"org_id":"org","workspace_id":"ws"})["allowed"] is False


def test_scheduler_execution_bridge_control(tmp_path):
    assert schedule_manifest()
    assert schedule_fire_plan("sched_health")["dry_run"] is True
    command = job_to_command({"job_type": "health_snapshot"})
    assert command.command == ("make", "health-trends")
    plan = execution_bridge_plan({"id":"job1", "job_type":"health_snapshot"})
    assert plan["safety"]["ok"] is True
    assert orchestrator_status()["ok"] is True
    db = tmp_path / "workers.db"
    q = WorkerJobQueue(db)
    q.enqueue("maintenance", "health_snapshot", "org_local", "ws_default")
    result = lease_and_plan_next("maintenance", "local-worker", str(db))
    assert result["ok"] is True
    assert result["leased"] is True
    fail = fail_job_policy(WorkerJob("j", "q", "health_snapshot", "org", "ws", attempts=3, max_attempts=3).to_dict())
    assert fail["decision"]["action"] == "dead_letter"


def test_ui_pages():
    assert "Worker Orchestration" in render_worker_overview()
    assert "Schedules" in render_schedules_page()
    assert "Worker Policy" in render_worker_policy_page()


def test_routes(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert route_worker_status()["ok"] is True
    assert route_worker_register_demo()["id"].startswith("worker_")
    assert route_worker_enqueue_demo()["id"].startswith("job_")
    assert route_worker_lease_demo()["leased"]["status"] == "leased"
    assert route_worker_schedules()["schedules"]
    assert route_worker_schedule_fire("sched_health")["dry_run"] is True
    assert route_worker_policy()["tenant_scoped"] is True
    assert route_worker_tenant_guard()["allowed"] is True
    assert route_worker_execution_bridge()["dry_run"] is True
    assert route_worker_lease_and_plan()["ok"] is True
    assert route_worker_fail_policy()["decision"]
    assert "events" in route_worker_audit()
    assert route_worker_page()["content_type"] == "text/html"
    assert route_worker_schedules_page()["content_type"] == "text/html"
    assert route_worker_policy_page()["content_type"] == "text/html"


def test_docs_scripts_assets_exist():
    root = Path(__file__).resolve().parents[1]
    for rel in [
        "scripts/workers/worker-status.sh",
        "scripts/workers/worker-register-demo.sh",
        "scripts/workers/worker-enqueue-demo.sh",
        "scripts/workers/worker-lease-demo.sh",
        "scripts/workers/worker-schedules.sh",
        "scripts/workers/worker-policy.sh",
        "scripts/workers/worker-tenant-guard.sh",
        "scripts/workers/worker-execution-bridge.sh",
        "scripts/workers/worker-lease-and-plan.sh",
        "scripts/workers/worker-fail-policy.sh",
        "scripts/workers/worker-audit.sh",
        "scripts/workers/worker-dashboard-export.sh",
        "deploy/workers/worker.example.env",
        "docs/workers/WORKER_ORCHESTRATION_GUIDE.md",
        "docs/workers/WORKER_QUEUE_AND_LEASES.md",
        "docs/workers/WORKER_TENANT_GUARD.md",
        "docs/workers/WORKER_EXECUTION_BRIDGE.md",
        "docs/workers/WORKER_RETRY_DEADLETTER.md",
        "docs/requirements/NEXT_V25_WORKER_ORCHESTRATION_REQUIREMENTS.md",
        "assets/workers/worker_orchestration_features.json",
    ]:
        assert (root / rel).exists(), rel
