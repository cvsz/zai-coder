from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable, Optional

from .actions import COMMAND_REGISTRY, ActionSpec, resolve_action

@dataclass
class TuiCommandDecision:
    action: Optional[ActionSpec]
    status: str  # allowed, blocked, needs_confirmation, unknown
    reason: str = ""

def route_tui_command(text: str) -> TuiCommandDecision:
    text = text.strip()
    if not text:
        return TuiCommandDecision(None, "unknown", "Empty command")

    parts = text.split()
    cmd = parts[0].lower()
    
    # Simple routing logic for now
    if cmd == "help":
        return TuiCommandDecision(None, "allowed", "Redirect to help screen")
    elif cmd == "palette":
        return TuiCommandDecision(None, "allowed", "Show command palette")
    elif cmd == "refresh":
        return TuiCommandDecision(None, "allowed", "Refresh UI")
    elif cmd == "quit":
        return TuiCommandDecision(None, "allowed", "Quit TUI")
    elif cmd == "dry-run":
        return TuiCommandDecision(None, "allowed", "Toggle dry run")

    # Try to resolve as registered action
    try:
        spec = resolve_action(text)
        return TuiCommandDecision(spec, "allowed", "Safe local action")
    except ValueError:
        return TuiCommandDecision(None, "unknown", f"Unknown command: {cmd}")

def list_tui_actions() -> list[ActionSpec]:
    return list(COMMAND_REGISTRY.values())
