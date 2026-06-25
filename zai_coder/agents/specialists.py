from __future__ import annotations

from .base import Agent, AgentContext


class TemplateAgent(Agent):
    role = "assistant"
    guardrails = "Never suggest git add . Never suggest --no-verify. Never force push. Never touch apps/zlms/**."

    def build_prompt(self, context: AgentContext) -> str:
        memory = "\n".join(f"- {k}: {v}" for k, v in context.memory.items())
        return f"""
Task: {context.task}

Project memory:
{memory or '- none'}

Act as the {self.role}. {self.guardrails}
Return concise, exact, actionable steps with validation commands.
""".strip()


class ArchitectAgent(TemplateAgent):
    name = "architect"
    description = "Designs system architecture, module boundaries, and migration plans."
    role = "enterprise software architect"


class DebuggerAgent(TemplateAgent):
    name = "debugger"
    description = "Finds root causes from logs, stack traces, and failing commands."
    role = "debugging specialist"


class TesterAgent(TemplateAgent):
    name = "tester"
    description = "Creates validation strategy, test commands, and coverage plans."
    role = "test engineer"


class SecurityAgent(TemplateAgent):
    name = "security"
    description = "Reviews commands, diffs, auth, secrets, and supply-chain risks."
    role = "security auditor"


class DevOpsAgent(TemplateAgent):
    name = "devops"
    description = "Handles Docker, CI/CD, systemd, Cloudflare, deployment, and observability."
    role = "DevOps and platform engineer"


class DocsAgent(TemplateAgent):
    name = "docs"
    description = "Writes READMEs, runbooks, operator guides, and changelogs."
    role = "technical documentation writer"


class ProductAgent(TemplateAgent):
    name = "product"
    description = "Turns broad goals into roadmap, features, phases, and acceptance criteria."
    role = "technical product manager"


class MediaDirectorAgent(TemplateAgent):
    name = "media-director"
    description = "Plans video, voice, music, image, and animation generation pipelines."
    role = "AI media director"
