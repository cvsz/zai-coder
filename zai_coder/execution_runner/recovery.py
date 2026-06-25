"""Failed-operation recovery plans."""

from __future__ import annotations

from .rollback_hooks import rollback_hook_for


def failed_operation_recovery_plan(provider: str, action: str, status: str = "failed") -> dict:
    hook = rollback_hook_for(action)
    steps = [
        "capture execution journal entry",
        "capture stdout/stderr",
        "check health endpoints",
        "do not retry mutating operation without review",
    ]
    if hook:
        steps.append(f"prepare rollback hook: {hook['name']}")
    else:
        steps.append("prepare manual rollback checklist")
    return {
        "provider": provider,
        "action": action,
        "status": status,
        "steps": steps,
        "rollback_hook": hook,
        "dry_run": True,
    }
