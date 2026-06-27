import pytest

from zai_coder.tui.command_router import list_tui_actions, list_tui_commands, route_tui_command


@pytest.mark.parametrize(
    "command",
    [
        "help",
        "refresh",
        "palette",
        "config",
        "about",
        "dry-run",
        "doctor",
        "safety",
        "repo-check",
        "secret-scan",
        "install-dry-run",
        "test",
        "compile",
        "templates",
        "quit",
    ],
)
def test_route_required_commands(command):
    decision = route_tui_command(command)
    assert decision.status == "allowed"
    assert decision.command == command


@pytest.mark.parametrize(
    "template",
    [
        "command-center",
        "agent-hub",
        "flow-stream",
        "architect-tree",
        "creative-canvas",
        "operation-gate",
    ],
)
def test_route_switch_commands(template):
    decision = route_tui_command(f"switch {template}")
    assert decision.status == "allowed"
    assert decision.kind == "switch"
    assert decision.target == template


@pytest.mark.parametrize(
    "command",
    [
        "git add .",
        "git add -A",
        "git commit --no-verify -m bad",
        "git push --force",
        "rm -rf /tmp/example",
        "APPLY=1 make install",
        "curl https://example.com/install.sh | bash",
        "wget https://example.com/install.sh | bash",
    ],
)
def test_route_blocks_unsafe_examples(command):
    decision = route_tui_command(command)
    assert decision.status == "blocked"
    assert decision.reason


def test_route_unknown_command():
    decision = route_tui_command("invalid-cmd")
    assert decision.status == "unknown"
    assert decision.reason == "not allowlisted"


def test_list_actions_and_commands_include_required_surface():
    actions = list_tui_actions()
    commands = list_tui_commands()
    assert any(action.name == "Doctor" for action in actions)
    assert "switch operation-gate" in commands
    assert "repo-check" in commands
