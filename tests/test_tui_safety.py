import pytest

from zai_coder.tui.safety import assert_allowed_tui_command, is_mutating_command, redact_secret_text


@pytest.mark.parametrize(
    "command",
    [
        ["git", "push", "origin", "main"],
        ["gh", "release", "create", "v1"],
        ["terraform", "apply"],
        ["kubectl", "apply", "-f", "x.yaml"],
        ["docker", "push", "repo/image"],
        ["cloudflare", "deploy"],
        ["stripe", "listen"],
        ["make", "safety-check", "APPLY=1"],
        ["echo", "API_KEY=abc123"],
    ],
)
def test_safety_blocks_forbidden_commands(command):
    assert is_mutating_command(command) is True
    with pytest.raises(ValueError):
        assert_allowed_tui_command(command)


def test_allowed_local_commands_pass():
    for command in (
        ["./run.sh", "doctor"],
        ["make", "safety-check"],
        ["make", "final-release-status"],
        ["make", "install-dry-run"],
        ["./run.sh", "tui", "--print-config"],
    ):
        assert_allowed_tui_command(command)


def test_unregistered_command_blocks():
    with pytest.raises(ValueError, match="not registered"):
        assert_allowed_tui_command(["python3", "-m", "pytest"])


def test_safety_redacts_secret_like_text():
    text = "token=abc123 password: hunter2 sk-liveabc123456789"
    redacted = redact_secret_text(text)
    assert "abc123" not in redacted
    assert "hunter2" not in redacted
    assert "liveabc" not in redacted
    assert "REDACTED" in redacted
