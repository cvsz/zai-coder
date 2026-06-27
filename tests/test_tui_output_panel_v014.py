from zai_coder.tui.actions import ActionResult
from zai_coder.tui.output import OutputPanel, format_action_result, format_output_panel


def test_output_panel_tracks_last_output():
    panel = OutputPanel(id="output")
    panel.update_output("hello")
    assert panel.last_output == "hello"


def test_format_output_panel_redacts_and_bounds():
    rendered = format_output_panel(["token=abc123", "safe"])
    assert "abc123" not in rendered
    assert "REDACTED" in rendered
    assert "safe" in rendered


def test_format_action_result_includes_status_and_command():
    result = ActionResult("Repo Check", ["make", "repo-check"], True, 0, stdout="[DRY-RUN] Would execute")
    rendered = format_action_result(result)
    assert "Repo Check: OK" in rendered
    assert "command: make repo-check" in rendered
    assert "[DRY-RUN]" in rendered
