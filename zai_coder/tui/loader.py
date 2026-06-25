from __future__ import annotations

from zai_coder.tui.templates.command_center import CommandCenterTemplate
from zai_coder.tui.templates.agent_hub import AgentHubTemplate
from zai_coder.tui.templates.flow_stream import FlowStreamTemplate
from zai_coder.tui.templates.architect_tree import ArchitectTreeTemplate
from zai_coder.tui.templates.creative_canvas import CreativeCanvasTemplate
from zai_coder.tui.templates.operation_gate import OperationGateTemplate

TEMPLATES = {
    "command-center": CommandCenterTemplate,
    "agent-hub": AgentHubTemplate,
    "flow-stream": FlowStreamTemplate,
    "architect-tree": ArchitectTreeTemplate,
    "creative-canvas": CreativeCanvasTemplate,
    "operation-gate": OperationGateTemplate
}

ROUTE_ALIASES = {
    "tui-template-01": "command-center",
    "tui-template-02": "agent-hub",
    "tui-template-03": "flow-stream",
    "tui-template-04": "architect-tree",
    "tui-template-05": "creative-canvas",
    "tui-template-06": "operation-gate",
}


def load_template(name: str, state=None):
    name = normalize_template_name(name)
    if name not in TEMPLATES:
        available = ", ".join(list_templates())
        raise ValueError(f"Unknown TUI template '{name}'. Available templates: {available}")
    return TEMPLATES[name](state=state)


def list_templates() -> list[str]:
    return list(TEMPLATES.keys())


def template_entries() -> list[dict[str, str]]:
    entries = []
    for name in list_templates():
        template = load_template(name)
        entries.append({"route_id": template.route_id, "name": template.name, "purpose": template.purpose})
    return entries


def normalize_template_name(name: str) -> str:
    normalized = str(name or "command-center").strip().lower().replace("_", "-").replace(" ", "-")
    return ROUTE_ALIASES.get(normalized, normalized)
