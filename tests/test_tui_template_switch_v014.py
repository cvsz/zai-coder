import json

import pytest

from zai_coder.tui.app import run_tui, submit_tui_command
from zai_coder.tui.config import TuiConfig
from zai_coder.tui.persistence import load_persisted_state
from zai_coder.tui.state import TuiState
from zai_coder.tui.template_controller import TemplateController, switch_active_template


def test_template_controller_switches_and_persists(tmp_path):
    state = TuiState(workspace=str(tmp_path))
    config = TuiConfig(state_path=".zai-coder/tui-state.json", persist_state=True)
    result = TemplateController(state, config, tmp_path).switch("operation-gate")

    loaded = load_persisted_state(tmp_path, ".zai-coder/tui-state.json")

    assert result.template == "operation-gate"
    assert result.persisted is True
    assert state.active_template == "operation-gate"
    assert loaded.active_template == "operation-gate"


def test_template_controller_respects_disabled_persistence(tmp_path):
    state = TuiState(workspace=str(tmp_path))
    config = TuiConfig(persist_state=False)
    result = switch_active_template(state, config, tmp_path, "agent-hub")

    assert result.template == "agent-hub"
    assert result.persisted is False
    assert state.active_template == "agent-hub"
    assert not (tmp_path / ".zai-coder" / "tui-state.json").exists()


def test_submit_switch_command_persists_immediately(tmp_path):
    state = TuiState(workspace=str(tmp_path))
    config = TuiConfig(state_path=".zai-coder/tui-state.json", persist_state=True)
    decision = submit_tui_command("switch creative-canvas", state, config, tmp_path)

    loaded = load_persisted_state(tmp_path, ".zai-coder/tui-state.json")

    assert decision.status == "allowed"
    assert state.active_template == "creative-canvas"
    assert loaded.active_template == "creative-canvas"
    assert "persisted" in state.last_result


def test_run_tui_uses_persisted_template_without_restart(tmp_path, capsys):
    state = TuiState(active_template="agent-hub", workspace=str(tmp_path))
    config = TuiConfig(state_path=".zai-coder/tui-state.json", persist_state=True)
    TemplateController(state, config, tmp_path).switch("agent-hub")

    assert run_tui(no_textual=True, root=tmp_path) == 0
    rendered = capsys.readouterr().out

    assert "Agent Hub" in rendered


def test_run_tui_uses_config_template_without_persisted_state(tmp_path, capsys):
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    (config_dir / "zai-coder.config.json").write_text(
        json.dumps({"tui": {"template": "operation-gate", "persist_state": False}}),
        encoding="utf-8",
    )

    assert run_tui(no_textual=True, root=tmp_path) == 0
    rendered = capsys.readouterr().out

    assert "Operation Gate" in rendered


def test_template_controller_rejects_unknown_template(tmp_path):
    with pytest.raises(ValueError, match="Unknown template"):
        TemplateController(TuiState(), TuiConfig(), tmp_path).switch("missing")
