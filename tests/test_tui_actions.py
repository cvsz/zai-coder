from zai_coder.tui.actions import list_actions, list_palette_commands, run_safe_action


def test_action_runner_dry_run_does_not_mutate():
    result = run_safe_action("doctor", dry_run=True)
    assert result.ok
    assert result.action_name == "Doctor"
    assert result.dry_run is True
    assert result.returncode == 0
    assert result.command == ["./run.sh", "doctor"]
    assert "[DRY-RUN]" in result.stdout
    assert result.duration_ms >= 0


def test_action_runner_blocks_unregistered_command():
    result = run_safe_action(["git", "push"], dry_run=True)
    assert result.blocked
    assert result.exit_code == 126
    assert result.reason


def test_command_palette_contains_required_items():
    palette = list_palette_commands()
    assert "Doctor" in palette
    assert "Switch: Operation Gate" in palette
    assert "Quit" in palette


def test_action_registry_contains_allowed_local_commands():
    commands = [" ".join(action.command) for action in list_actions()]
    assert "./run.sh doctor" in commands
    assert "make install-dry-run" in commands
