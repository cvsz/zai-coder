"""Project configuration JSON generator with presets and validation."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any
from zai_coder.config import ZaiConfig

PRESETS: dict[str, dict[str, Any]] = {
    "ollama": {
        "provider": "ollama",
        "base_url": "http://127.0.0.1:11434/v1",
        "model": "zcode-turbo-safe",
        "fallback_models": ["zcode-fast-safe", "zcode-qwen25-coder:14b-tiny"],
        "max_tokens": 2048,
        "temperature": 0.05,
        "safe_mode": True,
    },
    "openai": {
        "provider": "openai",
        "base_url": "https://api.openai.com/v1",
        "model": "gpt-4o-mini",
        "fallback_models": ["gpt-4-turbo", "gpt-3.5-turbo"],
        "max_tokens": 4096,
        "temperature": 0.1,
        "safe_mode": True,
    },
    "openrouter": {
        "provider": "openrouter",
        "base_url": "https://openrouter.ai/api/v1",
        "model": "google/gemini-2.5-flash",
        "fallback_models": ["meta-llama/llama-3.3-70b-instruct", "qwen/qwen-2.5-coder-32b-instruct"],
        "max_tokens": 4096,
        "temperature": 0.2,
        "safe_mode": True,
    },
}


class ProjectConfigGenerator:
    """Generates project configuration files with custom parameters and presets."""

    def __init__(self, output_path: str | Path | None = None):
        self.output_path = Path(output_path) if output_path else Path.home() / ".zai-coder" / "config.json"

    def generate_from_preset(self, preset_name: str, overrides: dict[str, Any] | None = None) -> ZaiConfig:
        if preset_name not in PRESETS:
            raise ValueError(f"Unknown preset: {preset_name}. Choose from: {', '.join(PRESETS.keys())}")
        
        config_data = dict(PRESETS[preset_name])
        if overrides:
            config_data.update(overrides)
            
        config = ZaiConfig.from_dict(config_data)
        self.save_config(config)
        return config

    def generate_custom(
        self,
        provider: str,
        base_url: str,
        model: str,
        fallback_models: list[str],
        workspace: str = ".",
        max_tokens: int = 2048,
        temperature: float = 0.05,
        safe_mode: bool = True,
        allow_apps_zlms: bool = False,
        tool_timeout_seconds: int = 180,
    ) -> ZaiConfig:
        config = ZaiConfig(
            provider=provider,
            base_url=base_url,
            model=model,
            fallback_models=fallback_models,
            workspace=workspace,
            max_tokens=max_tokens,
            temperature=temperature,
            safe_mode=safe_mode,
            allow_apps_zlms=allow_apps_zlms,
            tool_timeout_seconds=tool_timeout_seconds,
        )
        self.save_config(config)
        return config

    def save_config(self, config: ZaiConfig) -> None:
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        self.output_path.write_text(json.dumps(config.to_dict(), indent=2) + "\n", encoding="utf-8")
