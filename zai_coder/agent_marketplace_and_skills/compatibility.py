"""Agent/skill compatibility checks."""

from __future__ import annotations

from .catalog import find_skill, find_agent_listing


def compatibility_decision(agent_type: str, skill_id: str) -> dict:
    skill = find_skill(skill_id)
    allowed = agent_type in skill.compatible_agent_types
    return {
        "allowed": allowed,
        "agent_type": agent_type,
        "skill": skill.to_dict(),
        "reason": "compatible" if allowed else f"skill not compatible with agent_type={agent_type}",
    }


def agent_default_skill_plan(agent_id: str) -> dict:
    agent = find_agent_listing(agent_id)
    checks = [compatibility_decision(agent.agent_type, skill_id) for skill_id in agent.default_skills]
    return {"agent": agent.to_dict(), "checks": checks, "allowed": all(c["allowed"] for c in checks)}
