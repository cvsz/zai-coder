from zai_coder.tui.persistence import load_persisted_state, persist_template_selection, resolve_state_path
from zai_coder.tui.state import TuiState


def test_resolve_state_path_allows_absolute_path(tmp_path):
    absolute = tmp_path / "state.json"
    assert resolve_state_path(tmp_path / "root", absolute) == absolute


def test_persist_template_selection_writes_state(tmp_path):
    state = TuiState(active_template="command-center")
    ok = persist_template_selection(tmp_path, ".zai-coder/tui-state.json", state, "flow-stream")

    loaded = load_persisted_state(tmp_path, ".zai-coder/tui-state.json")

    assert ok is True
    assert state.active_template == "flow-stream"
    assert loaded.active_template == "flow-stream"


def test_persisted_state_redacts_output_buffers(tmp_path):
    state = TuiState(last_result="token=abc123", output_buffer=["password=hunter2"])
    assert persist_template_selection(tmp_path, ".zai-coder/tui-state.json", state, "agent-hub") is True

    raw = (tmp_path / ".zai-coder" / "tui-state.json").read_text(encoding="utf-8")

    assert "abc123" not in raw
    assert "hunter2" not in raw
    assert "REDACTED" in raw
