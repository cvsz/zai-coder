from __future__ import annotations

from .base import Agent, AgentContext


class CoderAgent(Agent):
    name = "coder"
    description = "Produces implementation plans and minimal patches."

    def build_prompt(self, context: AgentContext) -> str:
        plan = context.memory.get("planner", "")
        return f"""
Task: {context.task}

Planner context:
{plan}

Act as a safe coding agent. Return exact file paths, patch strategy, commands, and tests.
Never suggest broad staging or bypassing checks.
""".strip()
