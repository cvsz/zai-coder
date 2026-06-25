from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Iterable

from .messages import Message


@dataclass
class ModelResponse:
    content: str
    model: str
    provider: str
    ok: bool = True
    error: str = ""


class ModelProvider:
    name = "base"

    def chat(self, messages: list[Message], model: str, temperature: float = 0.05, max_tokens: int = 2048) -> ModelResponse:
        raise NotImplementedError


class EchoProvider(ModelProvider):
    name = "echo"

    def chat(self, messages: list[Message], model: str, temperature: float = 0.05, max_tokens: int = 2048) -> ModelResponse:
        last = next((m.content for m in reversed(messages) if m.role == "user"), "")
        return ModelResponse(
            content=(
                "[offline echo provider]\n"
                "No model endpoint responded. Task received:\n"
                f"{last}\n\n"
                "Suggested safe next commands:\n"
                "- git status --short\n"
                "- git diff --stat\n"
                "- run targeted tests after inspecting changed files\n"
            ),
            model=model,
            provider=self.name,
        )


class OpenAICompatibleProvider(ModelProvider):
    name = "openai-compatible"

    def __init__(self, base_url: str, api_key: str | None = None, provider_name: str | None = None, timeout: int = 120):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout
        if provider_name:
            self.name = provider_name

    def chat(self, messages: list[Message], model: str, temperature: float = 0.05, max_tokens: int = 2048) -> ModelResponse:
        payload = {
            "model": model,
            "messages": [m.to_dict() for m in messages],
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": False,
        }
        body = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            f"{self.base_url}/chat/completions",
            data=body,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        if self.api_key:
            req.add_header("Authorization", f"Bearer {self.api_key}")
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            content = data["choices"][0]["message"]["content"]
            return ModelResponse(content=content, model=model, provider=self.name)
        except Exception as exc:  # noqa: BLE001
            return ModelResponse(content="", model=model, provider=self.name, ok=False, error=str(exc))


class ModelRouter:
    def __init__(self, provider: ModelProvider, fallback_provider: ModelProvider | None = None):
        self.provider = provider
        self.fallback_provider = fallback_provider or EchoProvider()

    def chat_with_fallbacks(
        self,
        messages: list[Message],
        model: str,
        fallback_models: list[str] | None = None,
        temperature: float = 0.05,
        max_tokens: int = 2048,
    ) -> ModelResponse:
        tried: list[str] = []
        first = self.provider.chat(messages, model=model, temperature=temperature, max_tokens=max_tokens)
        if first.ok:
            return first
        tried.append(f"{model}: {first.error}")
        for fallback_model in fallback_models or []:
            response = self.provider.chat(messages, model=fallback_model, temperature=temperature, max_tokens=max_tokens)
            if response.ok:
                return response
            tried.append(f"{fallback_model}: {response.error}")
        echo = self.fallback_provider.chat(messages, model="echo", temperature=temperature, max_tokens=max_tokens)
        echo.content += "\n\nModel routing failures:\n" + "\n".join(f"- {t}" for t in tried)
        return echo


def provider_from_config(provider: str, base_url: str) -> ModelProvider:
    if provider in {"ollama", "ollama-launch", "local"}:
        return OpenAICompatibleProvider(base_url=base_url, provider_name="ollama")
    if provider == "openrouter":
        key = os.environ.get("OPENROUTER_API_KEY")
        return OpenAICompatibleProvider(base_url=base_url or "https://openrouter.ai/api/v1", api_key=key, provider_name="openrouter")
    if provider in {"openai", "openai-compatible"}:
        key = os.environ.get("OPENAI_API_KEY")
        return OpenAICompatibleProvider(base_url=base_url, api_key=key, provider_name=provider)
    return EchoProvider()
