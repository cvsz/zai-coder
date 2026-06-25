"""Execution runner routes."""

from __future__ import annotations

from zai_coder.execution_runner.models import CommandSpec
from zai_coder.execution_runner.queue import ExecutionQueue
from zai_coder.execution_runner.runner import ApprovedCommandRunner
from zai_coder.execution_runner.journal import ExecutionJournal
from zai_coder.execution_runner.rollback_hooks import list_rollback_hooks, rollback_hook_for
from zai_coder.execution_runner.recovery import failed_operation_recovery_plan
from zai_coder.execution_runner.approval_dashboard import render_approval_dashboard, approval_token_plan
from zai_coder.execution_runner.audit_timeline import render_execution_timeline
from zai_coder.execution_runner.safety import command_safety_report
from zai_coder.execution_runner.timeout_policy import TimeoutPolicy
from zai_coder.execution_runner.retry_policy import ExecutionRetryPolicy


def route_execution_status() -> dict:
    return {
        "ok": True,
        "service": "zai-execution-runner",
        "systems": [
            "approved_command_runner",
            "provider_operation_queue",
            "apply_execution_journal",
            "command_timeout_policy",
            "stdout_stderr_capture",
            "rollback_hook_registry",
            "retry_policy",
            "human_approval_dashboard",
            "execution_audit_timeline",
            "failed_operation_recovery_plan",
        ],
    }


def route_command_safety(payload: dict) -> dict:
    return command_safety_report(tuple(payload.get("command", [])), payload.get("cwd", "."))


def route_enqueue(payload: dict) -> dict:
    command = CommandSpec(
        command=tuple(payload.get("command", ["echo", "hello"])),
        cwd=payload.get("cwd", "."),
        timeout_seconds=int(payload.get("timeout_seconds", 60)),
        apply=bool(payload.get("apply", False)),
        approval_id=payload.get("approval_id", ""),
    )
    item = ExecutionQueue().enqueue(payload.get("provider", "local"), payload.get("action", "demo"), command)
    return item.to_dict()


def route_run_next() -> dict:
    queue = ExecutionQueue()
    item = queue.next_item()
    if item is None:
        return {"ok": True, "ran": False, "reason": "queue-empty"}
    queue.mark_status(item.id, "running", item.attempts + 1)
    result = ApprovedCommandRunner().run_item(item)
    queue.mark_status(item.id, "completed" if result.ok else result.status, item.attempts + 1)
    return {"ok": result.ok, "ran": True, "result": result.to_dict()}


def route_journal(limit: int = 50) -> dict:
    return {"events": ExecutionJournal().list_events(limit)}


def route_rollback_hooks() -> dict:
    return {"hooks": list_rollback_hooks()}


def route_rollback_hook(action: str) -> dict:
    return {"hook": rollback_hook_for(action)}


def route_recovery_plan(provider: str = "local", action: str = "unknown", status: str = "failed") -> dict:
    return failed_operation_recovery_plan(provider, action, status)


def route_approval_plan(reason: str = "manual-review") -> dict:
    return approval_token_plan(reason)


def route_approval_dashboard() -> dict:
    return {"content_type": "text/html", "html": render_approval_dashboard([])}


def route_execution_timeline() -> dict:
    return {"content_type": "text/html", "html": render_execution_timeline(ExecutionJournal().list_events())}


def route_timeout_policy() -> dict:
    return TimeoutPolicy().to_dict()


def route_retry_policy() -> dict:
    return ExecutionRetryPolicy().to_dict()
