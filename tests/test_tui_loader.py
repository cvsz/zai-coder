import pytest

from zai_coder.tui.loader import list_templates, load_template, normalize_template_name, template_entries


def test_all_templates_load():
    for name in (
        "command-center",
        "agent-hub",
        "flow-stream",
        "architect-tree",
        "creative-canvas",
        "operation-gate",
    ):
        template = load_template(name)
        assert template.name == name
        assert template.route_id.startswith("tui-template-")


def test_unknown_template_fails_clearly():
    with pytest.raises(ValueError, match="Unknown TUI template"):
        load_template("missing-template")


def test_list_templates_contains_all_six():
    assert list_templates() == [
        "command-center",
        "agent-hub",
        "flow-stream",
        "architect-tree",
        "creative-canvas",
        "operation-gate",
    ]


def test_route_ids_normalize_to_names():
    assert normalize_template_name("tui-template-01") == "command-center"
    assert normalize_template_name("Operation Gate") == "operation-gate"


def test_template_entries_include_ids_and_names():
    entries = template_entries()
    assert {"route_id": "tui-template-06", "name": "operation-gate", "purpose": entries[-1]["purpose"]} in entries
