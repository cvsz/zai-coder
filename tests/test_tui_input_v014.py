from zai_coder.tui.app import COMMAND_INPUT_ID, submit_tui_command
from zai_coder.tui.config import TuiConfig
from zai_coder.tui.state import TuiState


def test_command_input_contract_uses_bottom_command_id():
    assert COMMAND_INPUT_ID == "command"


def test_submit_command_records_history_and_outputs_help(tmp_path):
    state = TuiState(workspace=str(tmp_path))
    decision = submit_tui_command("help", state, TuiConfig(), tmp_path)

    assert decision.status == "allowed"
    assert state.last_command == "help"
    assert state.command_history[-1] == "help"
    assert "Command Center" in state.last_result
    assert state.output_buffer


def test_submit_action_uses_dry_run_safe_runner(tmp_path):
    state = TuiState(workspace=str(tmp_path))
    decision = submit_tui_command("repo-check", state, TuiConfig(), tmp_path)

    assert decision.status == "allowed"
    assert "Repo Check" in state.last_result
    assert "[DRY-RUN] Would execute: make repo-check" in state.last_result


def test_submit_switch_updates_active_template(tmp_path):
    state = TuiState(workspace=str(tmp_path))
    decision = submit_tui_command("switch agent-hub", state, TuiConfig(), tmp_path)

    assert decision.status == "allowed"
    assert state.active_template == "agent-hub"
    assert "Switched template to agent-hub" in state.last_result


def test_submit_blocked_command_is_not_executed(tmp_path):
    state = TuiState(workspace=str(tmp_path))
    decision = submit_tui_command("git add .", state, TuiConfig(), tmp_path)

    assert decision.status == "blocked"
    assert "BLOCKED" in state.last_result
    assert "git add ." in state.last_result
