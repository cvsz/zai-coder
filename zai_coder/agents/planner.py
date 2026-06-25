from __future__ import annotations

from .base import Agent, AgentContext


class PlannerAgent(Agent):
    name = "planner"
    description = "Breaks work into safe, staged execution plans."

    def build_prompt(self, context: AgentContext) -> str:
        return f"""
Task: {context.task}

Create a staged execution plan.
Rules:
- Inspect before editing.
- Prefer smallest safe patch.
- No git add .
- No git add -A.
- No --no-verify.
- No force push.
- Do not touch apps/zlms/**.
- Include validation commands.
""".strip()
