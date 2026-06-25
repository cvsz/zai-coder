from pathlib import Path
import tempfile
from datetime import datetime, timezone, timedelta

from zai_coder.agent_runtime_supervisor.models import AgentRuntime, AgentSandboxProfile, AgentTask, AgentBudget
from zai_coder.agent_runtime_supervisor.registry import AgentRegistry
from zai_coder.agent_runtime_supervisor.lifecycle import transition_decision, lifecycle_plan
from zai_coder.agent_runtime_supervisor.sandbox import DEFAULT_SANDBOX, sandbox_profile_manifest, sandbox_decision
from zai_coder.agent_runtime_supervisor.tasks import AgentTaskStore
from zai_coder.agent_runtime_supervisor.budget_guard import budget_decision, agent_permission_decision
from zai_coder.agent_runtime_supervisor.heartbeat import heartbeat_decision, heartbeat_policy
from zai_coder.agent_runtime_supervisor.crash_recovery import crash_recovery_plan, recovery_allowed
from zai_coder.agent_runtime_supervisor.worker_bridge import agent_task_worker_payload, worker_bridge_plan, enqueue_agent_task_job
from zai_coder.agent_runtime_supervisor.audit import AgentAuditLog
from zai_coder.agent_runtime_supervisor.control import supervisor_status, create_agent_demo, assign_task_demo, agent_start_gate
from zai_coder.agent_runtime_supervisor.ui.pages import render_agent_overview, render_agent_sandbox_page, render_agent_lifecycle_page, render_agent_policy_page
from zai_coder.agent_runtime_supervisor.routes import (
    route_agent_status,
    route_agent_supervisor_status,
    route_agent_create_demo,
    route_agent_assign_task_demo,
    route_agent_start_gate,
    route_agent_lifecycle_plan,
    route_agent_transition,
    route_agent_sandbox_profiles,
    route_agent_sandbox_decision,
    route_agent_budget_decision,
    route_agent_permission_decision,
    route_agent_heartbeat_policy,
    route_agent_crash_recovery,
    route_agent_audit,
    route_agent_page,
    route_agent_sandbox_page,
    route_agent_lifecycle_page,
    route_agent_policy_page,
)


def test_models_validation():
    assert AgentRuntime("a", "Agent", "builder", "org", "ws").validate() == []
    assert AgentRuntime("", "", "", "", "", status="bad", worker_queue="../x").validate()
    assert AgentSandboxProfile("s", "Sandbox").validate() == []
    assert AgentSandboxProfile("s", "Bad", "bad", "bad", 0).validate()
    assert AgentTask("t", "a", "org", "ws", "Title", "Instruction").validate() == []
    assert AgentTask("", "", "", "", "", "", status="bad", priority=-1).validate()
    assert AgentBudget("org", "ws").validate() == []


def test_registry_tasks_audit():
    with tempfile.TemporaryDirectory() as td:
        db = Path(td) / "agents.db"
        registry = AgentRegistry(db)
        agent = registry.register("Local Agent", "builder", "org", "ws")
        assert agent.id.startswith("agent_")
        assert registry.update_status(agent.id, "starting").status == "starting"
        assert registry.list_agents("org", "ws")[0]["id"] == agent.id
        store = AgentTaskStore(db)
        task = store.create_task(agent.id, "org", "ws", "Task", "Do safe planning.")
        assigned = store.assign_next(agent.id)
        assert assigned.id == task.id
        assert assigned.status == "assigned"
        assert store.list_tasks(agent.id)
        audit = AgentAuditLog(db)
        event = audit.record(agent.id, "org", "ws", "system", "agent.test", agent.id)
        assert audit.list_events(agent.id)[0]["id"] == event.id


def test_lifecycle_sandbox_budget_heartbeat_recovery():
    assert transition_decision("stopped", "starting")["allowed"] is True
    assert transition_decision("stopped", "running")["allowed"] is False
    assert lifecycle_plan("start")["dry_run"] is True
    assert sandbox_profile_manifest()
    assert sandbox_decision(DEFAULT_SANDBOX, "plan", "workspace/plan.md")["allowed"] is True
    assert sandbox_decision(DEFAULT_SANDBOX, "delete", "workspace/plan.md")["allowed"] is False
    assert sandbox_decision(DEFAULT_SANDBOX, "plan", ".env")["allowed"] is False
    budget = AgentBudget("org", "ws", max_tasks_per_day=1)
    assert budget_decision(budget, {"tasks": 1})["allowed"] is True
    assert budget_decision(budget, {"tasks": 2})["allowed"] is False
    assert agent_permission_decision(("agent_admin",), "start")["allowed"] is True
    old = (datetime.now(timezone.utc) - timedelta(seconds=999)).isoformat()
    assert heartbeat_decision(old)["stale"] is True
    assert heartbeat_policy()["heartbeat_required"] is True
    agent = {"id": "agent_demo", "status": "crashed"}
    assert crash_recovery_plan(agent)["dry_run"] is True
    assert recovery_allowed(agent, 0)["allowed"] is True
    assert recovery_allowed(agent, 3)["allowed"] is False


def test_worker_bridge_and_control(tmp_path):
    task = AgentTask("task1", "agent1", "org", "ws", "Title", "Instruction").to_dict()
    payload = agent_task_worker_payload(task)
    assert payload["safe_mode"] is True
    plan = worker_bridge_plan(task)
    assert plan["dry_run"] is True
    job = enqueue_agent_task_job(task, db_path=str(tmp_path / "workers.db"))
    assert job["job_type"] == "agent_task"
    assert supervisor_status()["ok"] is True
    assert create_agent_demo(str(tmp_path / "agents1.db"))["id"].startswith("agent_")
    assigned = assign_task_demo(str(tmp_path / "agents2.db"))
    assert assigned["bridge"]["job_type"] == "agent_task"
    assert agent_start_gate()["allowed"] is True


def test_ui_pages():
    assert "Agent Runtime Supervisor" in render_agent_overview()
    assert "Sandbox Profiles" in render_agent_sandbox_page()
    assert "Lifecycle" in render_agent_lifecycle_page()
    assert "Agent Policy" in render_agent_policy_page()


def test_routes(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert route_agent_status()["ok"] is True
    assert route_agent_supervisor_status()["ok"] is True
    assert route_agent_create_demo()["id"].startswith("agent_")
    assert route_agent_assign_task_demo()["bridge"]["job_type"] == "agent_task"
    assert route_agent_start_gate()["allowed"] is True
    assert route_agent_lifecycle_plan("start")["dry_run"] is True
    assert route_agent_transition("stopped", "starting")["allowed"] is True
    assert route_agent_sandbox_profiles()["profiles"]
    assert route_agent_sandbox_decision()["allowed"] is True
    assert route_agent_budget_decision()["allowed"] is True
    assert route_agent_permission_decision()["allowed"] is True
    assert route_agent_heartbeat_policy()["heartbeat_required"] is True
    assert route_agent_crash_recovery()["plan"]["dry_run"] is True
    assert "events" in route_agent_audit()
    assert route_agent_page()["content_type"] == "text/html"
    assert route_agent_sandbox_page()["content_type"] == "text/html"
    assert route_agent_lifecycle_page()["content_type"] == "text/html"
    assert route_agent_policy_page()["content_type"] == "text/html"


def test_docs_scripts_assets_exist():
    root = Path(__file__).resolve().parents[1]
    for rel in [
        "scripts/agents/agent-status.sh",
        "scripts/agents/agent-create-demo.sh",
        "scripts/agents/agent-assign-task-demo.sh",
        "scripts/agents/agent-start-gate.sh",
        "scripts/agents/agent-lifecycle-plan.sh",
        "scripts/agents/agent-sandbox-profiles.sh",
        "scripts/agents/agent-budget-guard.sh",
        "scripts/agents/agent-heartbeat-policy.sh",
        "scripts/agents/agent-crash-recovery.sh",
        "scripts/agents/agent-audit.sh",
        "scripts/agents/agent-dashboard-export.sh",
        "deploy/agents/agent-runtime.example.env",
        "docs/agents/AGENT_RUNTIME_SUPERVISOR_GUIDE.md",
        "docs/agents/AGENT_LIFECYCLE.md",
        "docs/agents/AGENT_SANDBOX_POLICY.md",
        "docs/agents/AGENT_TASK_ASSIGNMENT.md",
        "docs/agents/AGENT_CRASH_RECOVERY.md",
        "docs/requirements/NEXT_V26_AGENT_RUNTIME_SUPERVISOR_REQUIREMENTS.md",
        "assets/agents/agent_runtime_supervisor_features.json",
    ]:
        assert (root / rel).exists(), rel
