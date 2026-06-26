import pytest

from zai_coder.tui.navigation import TemplateNavigator, command_palette_entries, help_entries


def test_command_registry_includes_required_entries():
    labels = [entry.label for entry in command_palette_entries()]
    assert "Doctor" in labels
    assert "Safety Check" in labels
    assert "Switch: Command Center" in labels
    assert "Switch: Operation Gate" in labels


def test_template_navigator_switches_aliases():
    navigator = TemplateNavigator()
    assert navigator.switch("06") == "operation-gate"
    assert navigator.next_template() == "command-center"


def test_template_navigator_rejects_unknown_template():
    with pytest.raises(ValueError, match="Cannot switch"):
        TemplateNavigator().switch("missing")


def test_help_entries_are_template_specific():
    assert "ctrl+a" in help_entries("operation-gate")
    assert "ctrl+d" in help_entries("command-center")
