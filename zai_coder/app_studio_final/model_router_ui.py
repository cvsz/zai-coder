"""Model router UI model."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ModelRoute:
    task_type: str
    provider: str
    model: str
    priority: int = 100
    local_first: bool = True

    def validate(self) -> list[str]:
        issues = []
        if not self.task_type:
            issues.append("missing task_type")
        if not self.provider:
            issues.append("missing provider")
        if not self.model:
            issues.append("missing model")
        return issues

    def to_dict(self) -> dict:
        return {
            "task_type": self.task_type,
            "provider": self.provider,
            "model": self.model,
            "priority": self.priority,
            "local_first": self.local_first,
        }


DEFAULT_MODEL_ROUTES = [
    ModelRoute("coding", "ollama", "zcode-fast-safe", 10, True),
    ModelRoute("quick", "ollama", "zcode-turbo-safe", 20, True),
    ModelRoute("review", "ollama", "zcode-qwen25-coder:14b-tiny", 30, True),
]


def list_model_routes() -> list[dict]:
    return [route.to_dict() for route in DEFAULT_MODEL_ROUTES]
