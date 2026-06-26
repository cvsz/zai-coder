from zai_coder.tui.state import (
    TuiState,
    append_log,
    default_agent_tiles,
    default_gate_statuses,
    load_state,
    save_state,
    state_from_dict,
    state_to_dict,
    switch_template,
)


def test_tui_state_initializes_correctly():
    state = TuiState()
    assert state.active_template == "command-center"
    assert state.dry_run_mode is True
    assert len(state.agent_tiles) == 6
    assert state.gate_statuses


def test_default_agent_tiles_and_gate_statuses():
    assert [tile.name for tile in default_agent_tiles()] == [
        "Core Agent",
        "Release Agent",
        "Safety Agent",
        "Install Agent",
        "TUI Agent",
        "Memory Agent",
    ]
    assert [gate.name for gate in default_gate_statuses()] == [
        "Plan",
        "Dry Run",
        "Review",
        "Approval",
        "Apply",
        "Verify",
        "Rollback",
    ]


def test_state_persistence_save_load(tmp_path):
    path = tmp_path / ".zai-coder" / "tui-state.json"
    state = TuiState(active_template="operation-gate", last_focus="gate-pipeline", last_command="make tui-check")
    assert save_state(path, state) is True

    loaded = load_state(path)

    assert loaded.active_template == "operation-gate"
    assert loaded.last_focus == "gate-pipeline"
    assert loaded.last_command == "make tui-check"
    assert len(loaded.agent_tiles) == 6


def test_state_to_dict_redacts_secret_text():
    state = TuiState(last_command="echo token=abc123", last_result="password=hunter2")
    append_log(state, "API_KEY=abc123", level="warn")
    data = state_to_dict(state)
    assert "abc123" not in str(data)
    assert "hunter2" not in str(data)
    assert "REDACTED" in str(data)


def test_state_from_dict_and_switch_template():
    state = state_from_dict({"active_template": "command-center", "dry_run_mode": True})
    switch_template(state, "06")
    assert state.active_template == "operation-gate"
    assert state.last_focus == "template"
