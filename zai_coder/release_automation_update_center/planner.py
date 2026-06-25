"""Release planning."""

from __future__ import annotations

import uuid
from pathlib import Path

from .models import ReleasePlan, ReleaseVersion
from .versioning import next_version
from .channels import channel_policy


DEFAULT_CHECKS = (
    "python3 -m pytest -q",
    "make repo-check",
    "make secret-scan",
    "make production-api-gateway",
    "make worker-orchestration",
    "make agent-runtime-supervisor",
    "make plugin-connector-hub",
)


def create_release_plan(
    current_version: str = "v28.0.0",
    bump: str = "minor",
    channel: str = "stable",
    package_name: str = "zai-coder-control-plane",
    artifacts: tuple[str, ...] = ("dist/zai-coder-control-plane.zip",),
) -> ReleasePlan:
    policy = channel_policy(channel)
    release_version = next_version(current_version, bump, channel)
    checks = DEFAULT_CHECKS if policy["requires_full_tests"] else ("python3 -m pytest -q",)
    plan = ReleasePlan(
        id=f"relplan_{uuid.uuid4().hex[:12]}",
        version=release_version,
        package_name=package_name,
        artifacts=artifacts,
        checks=checks,
    )
    issues = plan.validate()
    if issues:
        raise ValueError("; ".join(issues))
    return plan


def release_readiness_check(plan: ReleasePlan, status: dict | None = None) -> dict:
    status = status or {}
    required = {
        "tests_passed": bool(status.get("tests_passed", False)),
        "repo_check_ok": bool(status.get("repo_check_ok", False)),
        "secret_scan_ok": bool(status.get("secret_scan_ok", False)),
        "artifacts_present": bool(status.get("artifacts_present", False)),
        "checksums_generated": bool(status.get("checksums_generated", False)),
        "rollback_plan_ready": bool(status.get("rollback_plan_ready", False)),
        "approval_present": bool(str(status.get("approval_id", "")).startswith("approved_")),
    }
    blocked = [key for key, ok in required.items() if not ok]
    return {"allowed": not blocked, "blocked": blocked, "required": required, "plan": plan.to_dict()}
