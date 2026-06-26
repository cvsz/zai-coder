import pytest

from zai_coder.tui.loader import (
    TemplateInfo,
    get_template_info,
    instantiate_template,
    list_templates,
    load_template,
    normalize_template_name,
    template_entries,
    template_names,
)
from zai_coder.tui.templates.base import BaseTemplate


def test_all_templates_load():
    for name in (
        "command-center",
        "agent-hub",
        "flow-stream",
        "architect-tree",
        "creative-canvas",
        "operation-gate",
    ):
        template_class = load_template(name)
        template = instantiate_template(name)
        assert issubclass(template_class, BaseTemplate)
        assert template.name == name
        assert template.route_id.startswith("tui-template-")


def test_unknown_template_fails_clearly():
    with pytest.raises(ValueError, match="Unknown TUI template"):
        load_template("missing-template")


def test_list_templates_contains_all_six():
    assert template_names() == [
        "command-center",
        "agent-hub",
        "flow-stream",
        "architect-tree",
        "creative-canvas",
        "operation-gate",
    ]
    assert all(isinstance(item, TemplateInfo) for item in list_templates())


def test_route_ids_normalize_to_names():
    assert normalize_template_name("tui-template-01") == "command-center"
    assert normalize_template_name("01") == "command-center"
    assert normalize_template_name("6") == "operation-gate"
    assert normalize_template_name("Operation Gate") == "operation-gate"


def test_template_entries_include_ids_and_names():
    entries = template_entries()
    assert {
        "route_id": "tui-template-06",
        "name": "operation-gate",
        "title": "Operation Gate",
        "purpose": entries[-1]["purpose"],
    } in entries


def test_get_template_info():
    info = get_template_info("02")
    assert info.route_id == "tui-template-02"
    assert info.name == "agent-hub"
