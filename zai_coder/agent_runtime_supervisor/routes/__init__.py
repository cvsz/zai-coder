"""Agent runtime supervisor route registry."""

from __future__ import annotations

from zai_coder.agent_runtime_supervisor.control import supervisor_status, create_agent_demo, assign_task_demo, agent_start_gate
from zai_coder.agent_runtime_supervisor.registry import AgentRegistry
from zai_coder.agent_runtime_supervisor.tasks import AgentTaskStore
from zai_coder.agent_runtime_supervisor.audit import AgentAuditLog
from zai_coder.agent_runtime_supervisor.lifecycle import lifecycle_plan, transition_decision
from zai_coder.agent_runtime_supervisor.sandbox import sandbox_profile_manifest, sandbox_decision, DEFAULT_SANDBOX
from zai_coder.agent_runtime_supervisor.budget_guard import budget_decision, agent_permission_decision
from zai_coder.agent_runtime_supervisor.models import AgentBudget
from zai_coder.agent_runtime_supervisor.heartbeat import heartbeat_policy, heartbeat_decision
from zai_coder.agent_runtime_supervisor.crash_recovery import crash_recovery_plan, recovery_allowed
from zai_coder.agent_runtime_supervisor.ui.pages import render_agent_overview, render_agent_sandbox_page, render_agent_lifecycle_page, render_agent_policy_page


def route_agent_status() -> dict:
    return {
        "ok": True,
        "service": "zai-agent-runtime-supervisor",
        "systems": [
            "agent_registry",
            "lifecycle_supervisor",
            "heartbeat_monitor",
            "sandbox_profile_policy",
            "task_assignment",
            "budget_permission_guard",
            "crash_recovery",
            "worker_bridge",
            "agent_dashboard",
            "agent_audit_log",
        ],
    }


def route_agent_supervisor_status() -> dict:
    return supervisor_status()


def route_agent_create_demo() -> dict:
    return create_agent_demo()


def route_agent_assign_task_demo() -> dict:
    return assign_task_demo()


def route_agent_start_gate() -> dict:
    return agent_start_gate()


def route_agent_lifecycle_plan(action: str = "start") -> dict:
    return lifecycle_plan(action)


def route_agent_transition(current_status: str = "stopped", target_status: str = "starting") -> dict:
    return transition_decision(current_status, target_status)


def route_agent_sandbox_profiles() -> dict:
    return {"profiles": sandbox_profile_manifest()}


def route_agent_sandbox_decision() -> dict:
    return sandbox_decision(DEFAULT_SANDBOX, "plan", "workspace/plan.md")


def route_agent_budget_decision() -> dict:
    return budget_decision(AgentBudget("org_local", "ws_default"), {"tasks": 1, "runtime_minutes": 10, "provider_apply": 0})


def route_agent_permission_decision() -> dict:
    return agent_permission_decision(("agent_admin",), "start")


def route_agent_heartbeat_policy() -> dict:
    return heartbeat_policy()


def route_agent_crash_recovery() -> dict:
    agent = {"id": "agent_demo", "status": "crashed"}
    return {"plan": crash_recovery_plan(agent), "allowed": recovery_allowed(agent, 0)}


def route_agent_audit() -> dict:
    return {"events": AgentAuditLog().list_events()}


def route_agent_page() -> dict:
    return {"content_type": "text/html", "html": render_agent_overview()}


def route_agent_sandbox_page() -> dict:
    return {"content_type": "text/html", "html": render_agent_sandbox_page()}


def route_agent_lifecycle_page() -> dict:
    return {"content_type": "text/html", "html": render_agent_lifecycle_page()}


def route_agent_policy_page() -> dict:
    return {"content_type": "text/html", "html": render_agent_policy_page()}
