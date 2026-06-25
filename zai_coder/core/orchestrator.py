from __future__ import annotations

from dataclasses import dataclass

from .messages import Message
from .models import ModelRouter, ModelResponse
from ..agents.base import Agent, AgentContext


@dataclass
class OrchestratorResult:
    content: str
    steps: list[str]
    model: str
    provider: str


class MultiAgentOrchestrator:
    def __init__(self, router: ModelRouter, model: str, fallback_models: list[str] | None = None, temperature: float = 0.05, max_tokens: int = 2048):
        self.router = router
        self.model = model
        self.fallback_models = fallback_models or []
        self.temperature = temperature
        self.max_tokens = max_tokens

    def run(self, task: str, agents: list[Agent]) -> OrchestratorResult:
        steps: list[str] = []
        context = AgentContext(task=task, memory={})
        transcript: list[Message] = [Message("system", "You are a safe multi-agent software engineering orchestrator.")]
        transcript.append(Message("user", task))
        final_model = self.model
        final_provider = ""

        for agent in agents:
            steps.append(f"agent:{agent.name}:start")
            prompt = agent.build_prompt(context)
            messages = transcript + [Message("user", prompt)]
            response = self.router.chat_with_fallbacks(
                messages,
                model=self.model,
                fallback_models=self.fallback_models,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
            )
            final_model = response.model
            final_provider = response.provider
            context.memory[agent.name] = response.content
            transcript.append(Message("assistant", f"[{agent.name}]\n{response.content}"))
            steps.append(f"agent:{agent.name}:done")

        synthesis = self.router.chat_with_fallbacks(
            transcript + [Message("user", "Synthesize a concise final plan with safe exact commands and validation steps.")],
            model=self.model,
            fallback_models=self.fallback_models,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
        )
        return OrchestratorResult(content=synthesis.content, steps=steps, model=final_model, provider=final_provider or synthesis.provider)
