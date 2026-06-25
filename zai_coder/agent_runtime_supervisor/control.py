"""Agent runtime supervisor control helpers."""

from __future__ import annotations

from .registry import AgentRegistry
from .tasks import AgentTaskStore
from .audit import AgentAuditLog
from .models import AgentBudget
from .lifecycle import transition_decision, lifecycle_plan
from .budget_guard import budget_decision, agent_permission_decision
from .sandbox import DEFAULT_SANDBOX, sandbox_decision
from .worker_bridge import worker_bridge_plan


def supervisor_status() -> dict:
    return {
        "ok": True,
        "systems": [
            "agent_registry",
            "lifecycle_supervisor",
            "heartbeat_monitor",
            "sandbox_profiles",
            "task_assignment",
            "budget_guard",
            "permission_guard",
            "crash_recovery",
            "worker_bridge",
            "agent_audit_log",
        ],
    }


def create_agent_demo(db_path: str = "data/agent-runtime-supervisor.db") -> dict:
    registry = AgentRegistry(db_path)
    audit = AgentAuditLog(db_path)
    agent = registry.register("Local Agent", "builder", "org_local", "ws_default")
    audit.record(agent.id, agent.org_id, agent.workspace_id, "system", "agent.registered", agent.id, agent.to_dict())
    return agent.to_dict()


def assign_task_demo(db_path: str = "data/agent-runtime-supervisor.db") -> dict:
    registry = AgentRegistry(db_path)
    tasks = AgentTaskStore(db_path)
    agent = registry.register("Task Agent", "builder", "org_local", "ws_default")
    task = tasks.create_task(agent.id, agent.org_id, agent.workspace_id, "Plan release", "Create a dry-run release plan.")
    assigned = tasks.assign_next(agent.id)
    bridge = worker_bridge_plan(assigned.to_dict()) if assigned else None
    return {"agent": agent.to_dict(), "task": task.to_dict(), "assigned": assigned.to_dict() if assigned else None, "bridge": bridge}


def agent_start_gate(roles: tuple[str, ...] = ("agent_admin",), usage: dict | None = None) -> dict:
    usage = usage or {"tasks": 1, "runtime_minutes": 10, "provider_apply": 0}
    budget = budget_decision(AgentBudget("org_local", "ws_default"), usage)
    permission = agent_permission_decision(roles, "start")
    sandbox = sandbox_decision(DEFAULT_SANDBOX, "plan", "workspace/plan.md")
    transition = transition_decision("stopped", "starting")
    allowed = budget["allowed"] and permission["allowed"] and sandbox["allowed"] and transition["allowed"]
    return {"allowed": allowed, "budget": budget, "permission": permission, "sandbox": sandbox, "transition": transition, "plan": lifecycle_plan("start")}
