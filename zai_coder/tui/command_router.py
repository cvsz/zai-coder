from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from .actions import ActionSpec, list_actions
from .loader import normalize_template_name, template_names
from .state import TuiState


@dataclass(frozen=True)
class TuiCommandDecision:
    status: str
    action: ActionSpec | None = None
    command: str = ""
    reason: str = ""


def list_tui_actions() -> list[ActionSpec]:
    return list_actions()


def route_tui_command(command_str: str) -> TuiCommandDecision:
    command = command_str.strip()
    if not command:
        return TuiCommandDecision("unknown", command="", reason="empty command")

    verb, *rest = command.split(maxsplit=1)
    verb = verb.lower()
    arg = rest[0] if rest else ""

    builtin_allowlist = {
        "help",
        "refresh",
        "palette",
        "config",
        "about",
        "dry-run",
        "doctor",
        "safety",
        "repo-check",
        "secret-scan",
        "install-dry-run",
        "test",
        "compile",
        "templates",
        "quit",
    }

    if verb == "switch":
        target = normalize_template_name(arg)
        if target in template_names():
            return TuiCommandDecision("allowed", command=command, reason=f"switch to {target}")
        return TuiCommandDecision("unknown", command=command, reason=f"unknown template: {arg}")

    if verb in builtin_allowlist:
        action = None
        if verb not in {"help", "refresh", "palette", "config", "about", "dry-run", "quit", "templates"}:
            try:
                action = next(item for item in list_actions() if item.name.lower().replace(" ", "-") == verb)
            except StopIteration:
                action = None
        return TuiCommandDecision("allowed", action=action, command=command, reason="allowlisted command")

    return TuiCommandDecision("unknown", command=command, reason="not allowlisted")


class TuiCommandRouter:
    def __init__(self, state: TuiState):
        self.state = state
        self._registry: dict[str, Callable[[str], Any]] = {}

    def register(self, command: str, action: Callable[[str], Any]) -> None:
        self._registry[command.strip().lower()] = action

    def route(self, command_str: str) -> Any:
        parts = command_str.strip().split(maxsplit=1)
        if not parts:
            self.state.add_log("Unknown command: ")
            return None

        command = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""

        if command in self._registry:
            self.state.add_log(f"Routing command: {command}")
            return self._registry[command](args)

        decision = route_tui_command(command_str)
        if decision.status == "allowed":
            self.state.add_log(f"Routing command: {command}")
            return decision

        self.state.add_log(f"Unknown command: {command}")
        return None
