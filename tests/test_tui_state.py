from zai_coder.tui.state import TuiState, default_agent_tiles, default_gate_statuses, load_state, save_state


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
