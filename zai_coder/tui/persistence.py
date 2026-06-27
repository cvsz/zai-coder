from __future__ import annotations

from pathlib import Path

from .state import TuiState, load_state, save_state


def resolve_state_path(root: str | Path, configured_path: str) -> Path:
    path = Path(configured_path)
    if path.is_absolute():
        return path
    return Path(root) / path


def load_persisted_state(root: str | Path, configured_path: str) -> TuiState:
    return load_state(resolve_state_path(root, configured_path))


def save_persisted_state(root: str | Path, configured_path: str, state: TuiState) -> bool:
    return save_state(resolve_state_path(root, configured_path), state)


def persist_template_selection(root: str | Path, configured_path: str, state: TuiState, template_name: str) -> bool:
    state.active_template = template_name
    return save_persisted_state(root, configured_path, state)
