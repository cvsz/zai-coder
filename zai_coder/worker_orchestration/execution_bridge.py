"""Bridge worker jobs to v18 approved execution runner commands."""

from __future__ import annotations

from zai_coder.execution_runner.models import CommandSpec
from zai_coder.execution_runner.safety import command_safety_report


JOB_COMMANDS = {
    "health_snapshot": ("make", "health-trends"),
    "backup_plan": ("make", "backup-plan"),
    "usage_aggregate": ("make", "usage-summary"),
    "gateway_smoke": ("make", "gateway-dispatch-demo"),
    "observability_export": ("make", "metrics-export"),
}


def job_to_command(job: dict) -> CommandSpec:
    job_type = job.get("job_type")
    if job_type not in JOB_COMMANDS:
        raise ValueError(f"unsupported job_type for execution bridge: {job_type}")
    return CommandSpec(command=JOB_COMMANDS[job_type], apply=False, timeout_seconds=120)


def execution_bridge_plan(job: dict) -> dict:
    spec = job_to_command(job)
    safety = command_safety_report(spec.command, spec.cwd)
    return {"dry_run": True, "job_id": job.get("id"), "command": spec.to_dict(), "safety": safety}
