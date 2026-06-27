from __future__ import annotations

import json
import sys
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from .safety import redact_secret_text


@dataclass
class AgentTile:
    name: str
    role: str
    status: str = "idle"
    summary: str = "Ready for local dry-run work."


@dataclass
class TimelineEvent:
    timestamp: str
    actor: str
    action: str
    status: str
    summary: str


@dataclass
class GateStatus:
    name: str
    status: str
    required_evidence: list[str]
    command_plan: list[str]
    approval_state: str = "not_requested"


@dataclass
class TuiState:
    active_template: str = "command-center"
    last_focus: str = "command-input"
    dry_run_mode: bool = True
    last_command: str = ""
    last_result: str = ""
    command_history: list[str] = field(default_factory=list)
    output_buffer: list[str] = field(default_factory=list)
    log_buffer: list[str] = field(default_factory=list)
    workspace: str = "."
    current_session: str = "local"
    agent_tiles: list[AgentTile] = field(default_factory=list)
    timeline_events: list[TimelineEvent] = field(default_factory=list)
    gate_statuses: list[GateStatus] = field(default_factory=list)
    refresh_timestamp: float = 0.0

    def __post_init__(self) -> None:
        if not self.agent_tiles:
            self.agent_tiles = default_agent_tiles()
        if not self.timeline_events:
            self.timeline_events = default_timeline_events()
        if not self.gate_statuses:
            self.gate_statuses = default_gate_statuses()
        if not self.refresh_timestamp:
            self.refresh_timestamp = time.time()

    @property
    def template(self) -> str:
        return self.active_template

    @template.setter
    def template(self, value: str) -> None:
        self.active_template = value

    @property
    def dry_run(self) -> bool:
        return self.dry_run_mode

    @dry_run.setter
    def dry_run(self, value: bool) -> None:
        self.dry_run_mode = value

    def add_log(self, message: str) -> None:
        self.log_buffer.append(redact_secret_text(message))
        self.log_buffer = self.log_buffer[-200:]
        self.refresh_timestamp = time.time()

    def record_command(self, command: str) -> None:
        redacted_command = redact_secret_text(command.strip())
        self.last_command = redacted_command
        if redacted_command:
            self.command_history.append(redacted_command)
            self.command_history = self.command_history[-200:]
        self.refresh_timestamp = time.time()

    def add_output(self, message: str) -> None:
        redacted_message = redact_secret_text(message)
        self.last_result = redacted_message
        self.output_buffer.append(redacted_message)
        self.output_buffer = self.output_buffer[-200:]
        self.refresh_timestamp = time.time()

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def default_agent_tiles() -> list[AgentTile]:
    return [
        AgentTile("Core Agent", "orchestration", "ready", "Routes local commands and session state."),
        AgentTile("Release Agent", "release", "ready", "Tracks release checks without publishing."),
        AgentTile("Safety Agent", "safety", "guarding", "Blocks external mutation and APPLY=1 commands."),
        AgentTile("Install Agent", "install", "ready", "Validates dry-run-first local install workflows."),
        AgentTile("TUI Agent", "interface", "active", "Owns template state and keyboard flows."),
        AgentTile("Memory Agent", "memory", "ready", "Persists local TUI state only."),
    ]


def default_timeline_events() -> list[TimelineEvent]:
    return [
        TimelineEvent(
            timestamp=time.strftime("%Y-%m-%dT%H:%M:%S"),
            actor="system",
            action="tui-ready",
            status="ready",
            summary="Local-first TUI state initialized.",
        )
    ]


def default_gate_statuses() -> list[GateStatus]:
    return [
        GateStatus("Plan", "ready", ["scope", "local command plan"], ["./run.sh tui --dry-run"], "not_required"),
        GateStatus("Dry Run", "ready", ["dry-run output"], ["make tui-check"], "not_required"),
        GateStatus("Review", "pending", ["git diff", "test output"], ["python3 -m pytest -q"], "not_requested"),
        GateStatus("Approval", "manual", ["human approval"], [], "required_before_apply"),
        GateStatus("Apply", "blocked", ["approval"], [], "blocked_by_default"),
        GateStatus("Verify", "pending", ["pytest", "safety-check"], ["make safety-check"], "not_requested"),
        GateStatus("Rollback", "ready", ["restore plan"], ["git restore <explicit-paths>"], "manual_only"),
    ]


def _coerce_agent_tiles(items: list[dict[str, Any]]) -> list[AgentTile]:
    return [AgentTile(**item) for item in items]


def _coerce_timeline_events(items: list[dict[str, Any]]) -> list[TimelineEvent]:
    return [TimelineEvent(**item) for item in items]


def _coerce_gate_statuses(items: list[dict[str, Any]]) -> list[GateStatus]:
    return [GateStatus(**item) for item in items]


def load_state(path: str | Path) -> TuiState:
    state_path = Path(path)
    if not state_path.exists():
        return TuiState()
    try:
        payload = json.loads(state_path.read_text(encoding="utf-8"))
        return state_from_dict(payload)
    except Exception as exc:  # pragma: no cover - defensive persistence guard
        print(f"WARN: failed to load TUI state from {state_path}: {exc}", file=sys.stderr)
        return TuiState()


def save_state(path: str | Path, state: TuiState) -> bool:
    state_path = Path(path)
    try:
        state_path.parent.mkdir(parents=True, exist_ok=True)
        state_path.write_text(json.dumps(state_to_dict(state), indent=2, sort_keys=True), encoding="utf-8")
        return True
    except Exception as exc:  # pragma: no cover - defensive persistence guard
        print(f"WARN: failed to save TUI state to {state_path}: {exc}", file=sys.stderr)
        return False


def state_to_dict(state: TuiState) -> dict[str, Any]:
    data = state.to_dict()
    data["last_command"] = redact_secret_text(data.get("last_command", ""))
    data["last_result"] = redact_secret_text(data.get("last_result", ""))
    data["command_history"] = [redact_secret_text(item) for item in data.get("command_history", [])][-200:]
    data["output_buffer"] = [redact_secret_text(item) for item in data.get("output_buffer", [])][-200:]
    data["log_buffer"] = [redact_secret_text(item) for item in data.get("log_buffer", [])][-200:]
    return data


def state_from_dict(data: dict[str, Any]) -> TuiState:
    payload = dict(data)
    payload["agent_tiles"] = _coerce_agent_tiles(payload.get("agent_tiles", []))
    payload["timeline_events"] = _coerce_timeline_events(payload.get("timeline_events", []))
    payload["gate_statuses"] = _coerce_gate_statuses(payload.get("gate_statuses", []))
    return TuiState(**payload)


def append_log(state: TuiState, message: str, level: str = "info") -> TuiState:
    state.add_log(f"{level.upper()}: {message}")
    return state


def switch_template(state: TuiState, template_name: str) -> TuiState:
    from .loader import normalize_template_name

    state.active_template = normalize_template_name(template_name)
    state.last_focus = "template"
    state.refresh_timestamp = time.time()
    return state
