import pytest
from zai_coder.tui.command_router import route_tui_command, list_tui_actions

def test_route_builtin_commands():
    assert route_tui_command("help").status == "allowed"
    assert route_tui_command("quit").status == "allowed"

def test_route_registered_action():
    decision = route_tui_command("doctor")
    assert decision.status == "allowed"
    assert decision.action is not None
    assert decision.action.name == "Doctor"

def test_route_unknown_command():
    decision = route_tui_command("invalid-cmd")
    assert decision.status == "unknown"

def test_list_actions():
    actions = list_tui_actions()
    assert len(actions) > 0
    assert any(a.name == "Doctor" for a in actions)
