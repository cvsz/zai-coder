"""Agent and skill catalog."""

from __future__ import annotations

from .models import SkillManifest, AgentListing


DEFAULT_SKILLS = [
    SkillManifest(
        "repo-planner",
        "Repository Planner",
        "1.0.0",
        "Creates safe repository plans.",
        "planning",
        tags=("git", "planning"),
        hermes_metadata={"tags": ["git", "planning"], "category": "planning"},
    ),
    SkillManifest(
        "release-checker",
        "Release Checker",
        "1.0.0",
        "Checks release readiness gates.",
        "release",
        required_permissions=("skill:view", "release:check"),
        tags=("release",),
        hermes_metadata={"tags": ["release"], "category": "release"},
    ),
    SkillManifest(
        "cloudflare-operator",
        "Cloudflare Operator",
        "1.0.0",
        "Plans Cloudflare Access and tunnel tasks.",
        "infrastructure",
        required_permissions=("skill:view", "providers:plan"),
        compatible_agent_types=("operator",),
        tags=("cloudflare",),
        hermes_metadata={"tags": ["cloudflare"], "category": "infrastructure", "requires_toolsets": ["terminal"]},
    ),
    SkillManifest(
        "billing-analyst",
        "Billing Analyst",
        "1.0.0",
        "Summarizes usage and invoice drafts.",
        "billing",
        required_permissions=("skill:view", "billing:view"),
        compatible_agent_types=("operator", "analyst"),
        tags=("billing",),
        hermes_metadata={"tags": ["billing"], "category": "billing"},
    ),
    SkillManifest(
        "hermes-skill-author",
        "Hermes Skill Author",
        "1.0.0",
        "Authors Hermes-compatible SKILL.md workflows.",
        "skills",
        required_permissions=("skill:view", "skill:install"),
        compatible_agent_types=("builder", "operator"),
        tags=("hermes", "skills", "skill.md"),
        platforms=("linux", "macos", "windows"),
        source="github",
        source_slug="cvsz/zai-coder/skills/hermes-skill-author",
        hermes_metadata={
            "tags": ["hermes", "skills", "skill.md"],
            "category": "skills",
            "requires_toolsets": ["terminal"],
        },
    ),
]

DEFAULT_AGENT_LISTINGS = [
    AgentListing("builder-agent", "Builder Agent", "builder", "Plans and builds local-first software changes.", ("repo-planner", "release-checker", "hermes-skill-author"), ("builder", "dev")),
    AgentListing("ops-agent", "Operations Agent", "operator", "Plans infra, deployment, backup, and health workflows.", ("cloudflare-operator", "release-checker"), ("ops", "infra")),
    AgentListing("billing-agent", "Billing Agent", "analyst", "Analyzes billing, usage, and quota state.", ("billing-analyst",), ("billing",)),
]


def skill_catalog() -> list[dict]:
    return [skill.to_dict() for skill in DEFAULT_SKILLS]


def agent_catalog() -> list[dict]:
    return [agent.to_dict() for agent in DEFAULT_AGENT_LISTINGS]


def find_skill(skill_id: str) -> SkillManifest:
    for skill in DEFAULT_SKILLS:
        if skill.id == skill_id:
            return skill
    raise ValueError(f"unknown skill: {skill_id}")


def find_agent_listing(agent_id: str) -> AgentListing:
    for agent in DEFAULT_AGENT_LISTINGS:
        if agent.id == agent_id:
            return agent
    raise ValueError(f"unknown agent listing: {agent_id}")


def search_catalog(query: str = "") -> dict:
    q = query.lower().strip()
    skills = [
        s.to_dict()
        for s in DEFAULT_SKILLS
        if not q
        or q in s.name.lower()
        or q in s.description.lower()
        or q in " ".join(s.tags).lower()
        or q in s.source.lower()
        or q in s.source_slug.lower()
    ]
    agents = [a.to_dict() for a in DEFAULT_AGENT_LISTINGS if not q or q in a.name.lower() or q in a.description.lower() or q in " ".join(a.tags).lower()]
    return {"query": query, "skills": skills, "agents": agents}
