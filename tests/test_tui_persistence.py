from zai_coder.tui.persistence import load_persisted_state, resolve_state_path, save_persisted_state
from zai_coder.tui.state import TuiState, load_state, save_state


def test_persistence_resolves_relative_state_path(tmp_path):
    assert resolve_state_path(tmp_path, ".zai-coder/tui-state.json") == tmp_path / ".zai-coder" / "tui-state.json"


def test_persisted_state_save_load(tmp_path):
    state = TuiState(active_template="agent-hub", last_result="ok")
    assert save_persisted_state(tmp_path, ".zai-coder/tui-state.json", state) is True

    loaded = load_persisted_state(tmp_path, ".zai-coder/tui-state.json")

    assert loaded.active_template == "agent-hub"
    assert loaded.last_result == "ok"


def test_persistence_failure_warns_but_does_not_crash(tmp_path, capsys):
    blocked_parent = tmp_path / "not-a-dir"
    blocked_parent.write_text("file", encoding="utf-8")

    assert save_state(blocked_parent / "state.json", TuiState()) is False
    assert "WARN: failed to save TUI state" in capsys.readouterr().err

    blocked_parent.write_text("{bad json", encoding="utf-8")
    loaded = load_state(blocked_parent)
    assert isinstance(loaded, TuiState)
    assert "WARN: failed to load TUI state" in capsys.readouterr().err
