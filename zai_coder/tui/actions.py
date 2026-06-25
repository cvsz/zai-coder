from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from .safety import assert_allowed_tui_command, redact_secret_text, require_dry_run_first


@dataclass(frozen=True)
class ActionSpec:
    name: str
    command: tuple[str, ...]
    description: str
    requires_dry_run: bool = True


@dataclass
class ActionResult:
    name: str
    command: list[str]
    exit_code: int
    stdout: str = ""
    stderr: str = ""
    dry_run: bool = True
    blocked: bool = False

    @property
    def ok(self) -> bool:
        return self.exit_code == 0 and not self.blocked


COMMAND_REGISTRY: dict[str, ActionSpec] = {
    "doctor": ActionSpec("Doctor", ("./run.sh", "doctor"), "Run local doctor checks."),
    "safety-check": ActionSpec("Safety Check", ("make", "safety-check"), "Run dry-run safety policy checks."),
    "final-release-status": ActionSpec(
        "Final Release Status",
        ("make", "final-release-status"),
        "Preview final release status without publishing.",
    ),
    "install-dry-run": ActionSpec("Install Dry Run", ("make", "install-dry-run"), "Preview local installer actions."),
    "tui-config": ActionSpec("TUI Config", ("./run.sh", "tui", "--print-config"), "Print resolved TUI config."),
}

PALETTE_COMMANDS = [
    "Doctor",
    "Safety Check",
    "Final Release Status",
    "Install Dry Run",
    "TUI Config",
    "Switch: Command Center",
    "Switch: Agent Hub",
    "Switch: Flow Stream",
    "Switch: Architect Tree",
    "Switch: Creative Canvas",
    "Switch: Operation Gate",
    "Help",
    "Quit",
]


def list_actions() -> list[ActionSpec]:
    return list(COMMAND_REGISTRY.values())


def list_palette_commands() -> list[str]:
    return list(PALETTE_COMMANDS)


def resolve_action(action: str | Iterable[str]) -> ActionSpec:
    if isinstance(action, str):
        key = action.strip().lower().replace(" ", "-")
        aliases = {
            "doctor": "doctor",
            "safety-check": "safety-check",
            "final-release-status": "final-release-status",
            "install-dry-run": "install-dry-run",
            "tui-config": "tui-config",
        }
        registry_key = aliases.get(key)
        if registry_key and registry_key in COMMAND_REGISTRY:
            return COMMAND_REGISTRY[registry_key]
        raise ValueError(f"Unknown TUI action: {action}")
    command = tuple(action)
    assert_allowed_tui_command(list(command))
    return ActionSpec("Custom Local Command", command, "Registered local-safe command.")


def run_safe_action(
    action: str | Iterable[str],
    dry_run: bool = True,
    cwd: str | Path | None = None,
    timeout: int = 60,
    dry_run_completed: bool = True,
) -> ActionResult:
    try:
        spec = resolve_action(action)
        command = list(spec.command)
        assert_allowed_tui_command(command)
        if not require_dry_run_first(spec.name, apply=not dry_run, dry_run_completed=dry_run_completed):
            raise ValueError(f"{spec.name} requires a completed dry run before execution.")
    except ValueError as exc:
        command = [action] if isinstance(action, str) else list(action)
        return ActionResult("Blocked TUI Action", command, 126, stderr=str(exc), dry_run=dry_run, blocked=True)

    if dry_run:
        return ActionResult(
            spec.name,
            command,
            0,
            stdout=f"[DRY-RUN] Would execute: {' '.join(command)}",
            dry_run=True,
        )

    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=timeout, cwd=cwd, check=False)
        return ActionResult(
            spec.name,
            command,
            result.returncode,
            stdout=redact_secret_text(result.stdout),
            stderr=redact_secret_text(result.stderr),
            dry_run=False,
        )
    except Exception as exc:  # pragma: no cover - defensive subprocess guard
        return ActionResult(spec.name, command, 1, stderr=f"Action failed: {exc}", dry_run=False)
