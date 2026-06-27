from __future__ import annotations

import subprocess
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from .safety import assert_allowed_tui_command, redact_secret_text, require_dry_run_first

REPO_ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class ActionSpec:
    name: str
    command: tuple[str, ...]
    description: str
    requires_dry_run: bool = True


@dataclass
class ActionResult:
    action_name: str
    command: list[str]
    dry_run: bool
    returncode: int
    stdout: str = ""
    stderr: str = ""
    duration_ms: int = 0
    blocked: bool = False
    reason: str = ""

    @property
    def name(self) -> str:
        return self.action_name

    @property
    def exit_code(self) -> int:
        return self.returncode

    @property
    def ok(self) -> bool:
        return self.returncode == 0 and not self.blocked


COMMAND_REGISTRY: dict[str, ActionSpec] = {
    "doctor": ActionSpec("Doctor", ("./run.sh", "doctor"), "Run local doctor checks."),
    "safety": ActionSpec("Safety", ("make", "safety-check"), "Run dry-run safety policy checks."),
    "safety-check": ActionSpec("Safety Check", ("make", "safety-check"), "Run dry-run safety policy checks."),
    "repo-check": ActionSpec("Repo Check", ("make", "repo-check"), "Run repository hygiene checks."),
    "secret-scan": ActionSpec("Secret Scan", ("make", "secret-scan"), "Run local secret scanning."),
    "final-release-status": ActionSpec(
        "Final Release Status",
        ("make", "final-release-status"),
        "Preview final release status without publishing.",
    ),
    "install-dry-run": ActionSpec("Install Dry Run", ("make", "install-dry-run"), "Preview local installer actions."),
    "test": ActionSpec("Test", ("python3", "-m", "pytest", "-q"), "Run the local pytest suite."),
    "compile": ActionSpec("Compile", ("python3", "-m", "compileall", "-q", "zai_coder"), "Compile Python sources."),
    "tui-config": ActionSpec("TUI Config", ("./run.sh", "tui", "--print-config"), "Print resolved TUI config."),
}

PALETTE_COMMANDS = [
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
    "Doctor",
    "Safety Check",
    "Repo Check",
    "Secret Scan",
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
            "safety": "safety",
            "safety-check": "safety-check",
            "repo-check": "repo-check",
            "secret-scan": "secret-scan",
            "final-release-status": "final-release-status",
            "install-dry-run": "install-dry-run",
            "test": "test",
            "compile": "compile",
            "config": "tui-config",
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
    started = time.monotonic()
    try:
        spec = resolve_action(action)
        command = list(spec.command)
        assert_allowed_tui_command(command)
        if not require_dry_run_first(spec.name, apply=not dry_run, dry_run_completed=dry_run_completed):
            raise ValueError(f"{spec.name} requires a completed dry run before execution.")
    except ValueError as exc:
        command = [action] if isinstance(action, str) else list(action)
        return ActionResult(
            action_name="Blocked TUI Action",
            command=command,
            dry_run=dry_run,
            returncode=126,
            stderr=str(exc),
            duration_ms=_duration_ms(started),
            blocked=True,
            reason=str(exc),
        )

    if dry_run:
        return ActionResult(
            action_name=spec.name,
            command=command,
            dry_run=True,
            returncode=0,
            stdout=f"[DRY-RUN] Would execute: {' '.join(command)}",
            duration_ms=_duration_ms(started),
        )

    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=timeout, cwd=cwd or REPO_ROOT, check=False)
        return ActionResult(
            action_name=spec.name,
            command=command,
            dry_run=False,
            returncode=result.returncode,
            stdout=redact_secret_text(result.stdout),
            stderr=redact_secret_text(result.stderr),
            duration_ms=_duration_ms(started),
        )
    except Exception as exc:  # pragma: no cover - defensive subprocess guard
        return ActionResult(
            action_name=spec.name,
            command=command,
            dry_run=False,
            returncode=1,
            stderr=f"Action failed: {exc}",
            duration_ms=_duration_ms(started),
            reason=str(exc),
        )


def _duration_ms(started: float) -> int:
    return int((time.monotonic() - started) * 1000)
