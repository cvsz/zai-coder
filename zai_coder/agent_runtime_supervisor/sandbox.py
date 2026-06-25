"""Agent sandbox profiles and checks."""

from __future__ import annotations

from .models import AgentSandboxProfile


DEFAULT_SANDBOX = AgentSandboxProfile(
    id="sandbox_default",
    name="Default Local Sandbox",
    network_mode="local-only",
    filesystem_mode="workspace-scoped",
    max_runtime_seconds=3600,
)


def sandbox_profile_manifest() -> list[dict]:
    return [
        DEFAULT_SANDBOX.to_dict(),
        AgentSandboxProfile("sandbox_readonly", "Read Only", "offline", "read-only", 1800, ("read", "plan")).to_dict(),
        AgentSandboxProfile("sandbox_ephemeral", "Ephemeral", "local-only", "ephemeral", 1200, ("read", "plan", "test")).to_dict(),
    ]


def sandbox_decision(profile: AgentSandboxProfile, requested_tool: str, requested_path: str = "") -> dict:
    issues = profile.validate()
    if issues:
        return {"allowed": False, "reason": "; ".join(issues), "profile": profile.to_dict()}
    if requested_tool not in profile.allowed_tools:
        return {"allowed": False, "reason": f"tool not allowed: {requested_tool}", "profile": profile.to_dict()}
    normalized = requested_path.replace("\\", "/")
    for blocked in profile.blocked_paths:
        if normalized.startswith(blocked) or blocked in normalized:
            return {"allowed": False, "reason": f"blocked path: {blocked}", "profile": profile.to_dict()}
    return {"allowed": True, "reason": "sandbox policy satisfied", "profile": profile.to_dict()}
