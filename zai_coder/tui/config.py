from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

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


def _normalize_template_value(name: str) -> str:
    normalized = str(name or "command-center").strip().lower().replace("_", "-").replace(" ", "-")
    aliases = {
        "tui-template-01": "command-center",
        "tui-template-02": "agent-hub",
        "tui-template-03": "flow-stream",
        "tui-template-04": "architect-tree",
        "tui-template-05": "creative-canvas",
        "tui-template-06": "operation-gate",
    }
    return aliases.get(normalized, normalized)


def load_tui_config(root: str | Path | None = None, config_path: str | Path | None = None) -> dict:
    project_root = Path(root or ".")
    path = Path(config_path) if config_path else project_root / "config" / "zai-coder.config.json"
    resolved = deepcopy(DEFAULT_TUI_CONFIG)
    if path.exists():
        payload = json.loads(path.read_text(encoding="utf-8"))
        tui_payload = payload.get("tui", {})
        if not isinstance(tui_payload, dict):
            raise ValueError(f"Invalid TUI config in {path}: expected object at key 'tui'")
        resolved.update(tui_payload)
    resolved["template"] = _normalize_template_value(resolved.get("template", "command-center"))
    resolved["refresh_interval_seconds"] = max(1, int(resolved.get("refresh_interval_seconds", 1)))
    resolved["dry_run_first"] = bool(resolved.get("dry_run_first", True))
    resolved["persist_state"] = bool(resolved.get("persist_state", True))
    return resolved
