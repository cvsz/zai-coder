from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from .actions import ActionSpec, list_actions, resolve_action
from .loader import normalize_template_name, template_names
from .safety import is_mutating_command
from .state import TuiState


BUILTIN_COMMANDS = {
    "help",
    "refresh",
    "palette",
    "config",
    "about",
    "dry-run",
    "templates",
    "quit",
}

ACTION_COMMANDS = {
    "doctor",
    "safety",
    "repo-check",
    "secret-scan",
    "install-dry-run",
    "test",
    "compile",
}


@dataclass(frozen=True)
class TuiCommandDecision:
    status: str
    command: str = ""
    kind: str = "unknown"
    reason: str = ""
    action: ActionSpec | None = None
    target: str = ""

    @property
    def allowed(self) -> bool:
        return self.status == "allowed"

    @property
    def blocked(self) -> bool:
        return self.status == "blocked"


def list_tui_actions() -> list[ActionSpec]:
    return list_actions()


def list_tui_commands() -> list[str]:
    return [
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
        "switch command-center",
        "switch agent-hub",
        "switch flow-stream",
        "switch architect-tree",
        "switch creative-canvas",
        "switch operation-gate",
        "quit",
    ]


def route_tui_command(command_str: str) -> TuiCommandDecision:
    command = command_str.strip()
    if not command:
        return TuiCommandDecision("unknown", command="", reason="empty command")

    if is_mutating_command(command.split()):
        return TuiCommandDecision("blocked", command=command, reason="blocked by TUI safety policy")

    verb, *rest = command.split(maxsplit=1)
    verb = verb.lower()
    arg = rest[0] if rest else ""

    if verb == "switch":
        if not arg:
            return TuiCommandDecision("unknown", command=command, kind="switch", reason="missing template")
        target = normalize_template_name(arg)
        if target in template_names():
            return TuiCommandDecision("allowed", command=command, kind="switch", reason=f"switch to {target}", target=target)
        return TuiCommandDecision("unknown", command=command, kind="switch", reason=f"unknown template: {arg}")

    if verb in BUILTIN_COMMANDS:
        return TuiCommandDecision("allowed", command=command, kind="builtin", reason="allowlisted command")

    if verb in ACTION_COMMANDS:
        try:
            action = resolve_action(verb)
        except ValueError as exc:
            return TuiCommandDecision("blocked", command=command, kind="action", reason=str(exc))
        return TuiCommandDecision("allowed", command=command, kind="action", reason="allowlisted action", action=action)

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
            return route_tui_command("")

        command = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""

        if command in self._registry:
            self.state.add_log(f"Routing command: {command}")
            return self._registry[command](args)

        decision = route_tui_command(command_str)
        if decision.allowed:
            self.state.add_log(f"Routing command: {command}")
        elif decision.blocked:
            self.state.add_log(f"Blocked command: {command}")
        else:
            self.state.add_log(f"Unknown command: {command}")
        return decision
