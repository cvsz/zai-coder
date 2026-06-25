from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

DEFAULT_CONFIG_PATH = Path.home() / ".zai-coder" / "config.json"


@dataclass
class ZaiConfig:
    provider: str = "ollama"
    base_url: str = "http://127.0.0.1:11434/v1"
    model: str = "zcode-turbo-safe"
    fallback_models: list[str] = field(default_factory=lambda: ["zcode-fast-safe", "zcode-qwen25-coder:14b-tiny"])
    workspace: str = "."
    max_tokens: int = 2048
    temperature: float = 0.05
    safe_mode: bool = True
    allow_apps_zlms: bool = False
    tool_timeout_seconds: int = 180

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ZaiConfig":
        known = {f.name for f in cls.__dataclass_fields__.values()}  # type: ignore[attr-defined]
        filtered = {k: v for k, v in data.items() if k in known}
        return cls(**filtered)

    def to_dict(self) -> dict[str, Any]:
        return {
            "provider": self.provider,
            "base_url": self.base_url,
            "model": self.model,
            "fallback_models": self.fallback_models,
            "workspace": self.workspace,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "safe_mode": self.safe_mode,
            "allow_apps_zlms": self.allow_apps_zlms,
            "tool_timeout_seconds": self.tool_timeout_seconds,
        }


def load_config(path: str | None = None) -> ZaiConfig:
    config_path = Path(path).expanduser() if path else DEFAULT_CONFIG_PATH
    env_model = os.environ.get("ZAI_CODER_MODEL")
    env_base_url = os.environ.get("ZAI_CODER_BASE_URL")
    if config_path.exists():
        data = json.loads(config_path.read_text(encoding="utf-8"))
        cfg = ZaiConfig.from_dict(data)
    else:
        cfg = ZaiConfig()
    if env_model:
        cfg.model = env_model
    if env_base_url:
        cfg.base_url = env_base_url
    return cfg


def ensure_config(path: str | None = None) -> Path:
    config_path = Path(path).expanduser() if path else DEFAULT_CONFIG_PATH
    config_path.parent.mkdir(parents=True, exist_ok=True)
    if not config_path.exists():
        config_path.write_text(json.dumps(ZaiConfig().to_dict(), indent=2) + "\n", encoding="utf-8")
    return config_path
