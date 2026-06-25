from __future__ import annotations

from .design_tokens import render_chip
from .state import AgentTile, GateStatus, TuiState


def render_agent_grid(tiles: list[AgentTile]) -> str:
    return "\n".join(f"[{tile.status.upper()}] {tile.name} - {tile.role}: {tile.summary}" for tile in tiles)


def render_gate_pipeline(gates: list[GateStatus]) -> str:
    return "\n".join(
        f"[{gate.status.upper()}] {gate.name}: approval={gate.approval_state}; evidence={', '.join(gate.required_evidence)}"
        for gate in gates
    )


def render_status_sidebar(state: TuiState) -> str:
    return "\n".join(
        [
            render_chip("Workspace", state.workspace, "ready"),
            render_chip("Dry Run", "on" if state.dry_run_mode else "off", "dry_run"),
            render_chip("Session", state.current_session, "active"),
            render_chip("Template", state.active_template, "ready"),
            render_chip("Last Command", state.last_command or "none", "neutral"),
        ]
    )
