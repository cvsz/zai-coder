from __future__ import annotations

from .base import Agent, AgentContext


class ReviewerAgent(Agent):
    name = "reviewer"
    description = "Reviews proposed work for safety, correctness, and validation gaps."

    def build_prompt(self, context: AgentContext) -> str:
        prior = "\n\n".join(f"## {k}\n{v}" for k, v in context.memory.items())
        return f"""
Task: {context.task}

Prior agent output:
{prior}

Review for:
- unsafe commands
- missing tests
- secret leaks
- unrelated changes
- apps/zlms/** violations
- generated artifact staging
Return final review notes and corrections.
""".strip()
