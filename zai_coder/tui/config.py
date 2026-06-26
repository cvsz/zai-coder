from __future__ import annotations

import json
from copy import deepcopy
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterator

DEFAULT_TUI_CONFIG = {
    "enabled": True,
    "template": "command-center",
    "dry_run_first": True,
    "refresh_interval_seconds": 1,
    "show_logs": True,
    "show_agent_grid": True,
    "persist_state": True,
    "state_path": ".zai-coder/tui-state.json",
    "theme": "zeaz-glass-dark"
}

VALID_TEMPLATES = {
    "command-center",
    "agent-hub",
    "flow-stream",
    "architect-tree",
    "creative-canvas",
    "operation-gate",
}

TEMPLATE_ALIASES = {
    "01": "command-center",
    "1": "command-center",
    "tui-template-01": "command-center",
    "02": "agent-hub",
    "2": "agent-hub",
    "tui-template-02": "agent-hub",
    "03": "flow-stream",
    "3": "flow-stream",
    "tui-template-03": "flow-stream",
    "04": "architect-tree",
    "4": "architect-tree",
    "tui-template-04": "architect-tree",
    "05": "creative-canvas",
    "5": "creative-canvas",
    "tui-template-05": "creative-canvas",
    "06": "operation-gate",
    "6": "operation-gate",
    "tui-template-06": "operation-gate",
}


@dataclass(frozen=True)
class TuiConfig:
    enabled: bool = True
    template: str = "command-center"
    dry_run_first: bool = True
    refresh_interval_seconds: int = 1
    show_logs: bool = True
    show_agent_grid: bool = True
    persist_state: bool = True
    state_path: str = ".zai-coder/tui-state.json"
    theme: str = "zeaz-glass-dark"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def get(self, key: str, default: Any = None) -> Any:
        return self.to_dict().get(key, default)

    def __getitem__(self, key: str) -> Any:
        return self.to_dict()[key]

    def __iter__(self) -> Iterator[str]:
        return iter(self.to_dict())


def _normalize_template_value(name: str) -> str:
    normalized = str(name or "command-center").strip().lower().replace("_", "-").replace(" ", "-")
    return TEMPLATE_ALIASES.get(normalized, normalized)


def load_tui_config(path: str | Path | None = None, *, root: str | Path | None = None, config_path: str | Path | None = None) -> TuiConfig:
    selected_path = config_path or path
    project_root = Path(root or ".")
    candidate = Path(selected_path) if selected_path else project_root / "config" / "zai-coder.config.json"
    return resolve_tui_config(candidate)


def resolve_tui_config(path: str | Path | None = None, overrides: dict[str, Any] | None = None) -> TuiConfig:
    config_path = Path(path) if path else Path("config") / "zai-coder.config.json"
    resolved = deepcopy(DEFAULT_TUI_CONFIG)
    if config_path.exists():
        payload = json.loads(config_path.read_text(encoding="utf-8"))
        tui_payload = payload.get("tui", {})
        if not isinstance(tui_payload, dict):
            raise ValueError(f"Invalid TUI config in {config_path}: expected object at key 'tui'")
        resolved.update(tui_payload)
    if overrides:
        resolved.update(overrides)
    resolved["template"] = _normalize_template_value(resolved.get("template", "command-center"))
    if resolved["template"] not in VALID_TEMPLATES:
        available = ", ".join(sorted(VALID_TEMPLATES))
        raise ValueError(f"Invalid TUI template in config: {resolved['template']}. Available templates: {available}")
    resolved["refresh_interval_seconds"] = max(1, int(resolved.get("refresh_interval_seconds", 1)))
    resolved["dry_run_first"] = bool(resolved.get("dry_run_first", True))
    resolved["persist_state"] = bool(resolved.get("persist_state", True))
    return TuiConfig(**resolved)
