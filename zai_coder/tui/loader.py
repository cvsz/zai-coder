from __future__ import annotations

from dataclasses import dataclass
from typing import Type

from zai_coder.tui.config import TEMPLATE_ALIASES
from zai_coder.tui.state import TuiState
from zai_coder.tui.templates.base import BaseTemplate
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
    **TEMPLATE_ALIASES,
    "tui-template-01": "command-center",
    "tui-template-02": "agent-hub",
    "tui-template-03": "flow-stream",
    "tui-template-04": "architect-tree",
    "tui-template-05": "creative-canvas",
    "tui-template-06": "operation-gate",
}


@dataclass(frozen=True)
class TemplateInfo:
    route_id: str
    name: str
    title: str
    purpose: str

    def __str__(self) -> str:
        return self.name

    def __eq__(self, other) -> bool:
        if isinstance(other, str):
            return self.name == other
        return super().__eq__(other)


def _template_class(name: str) -> Type[BaseTemplate]:
    normalized = normalize_template_name(name)
    if normalized not in TEMPLATES:
        available = ", ".join(info.name for info in list_templates())
        raise ValueError(f"Unknown TUI template: {name}. Available templates: {available}")
    return TEMPLATES[normalized]


def load_template(name: str) -> Type[BaseTemplate]:
    return _template_class(name)


def instantiate_template(name: str, state: TuiState | None = None) -> BaseTemplate:
    return load_template(name)(state=state)


def list_templates() -> list[TemplateInfo]:
    return [get_template_info(name) for name in TEMPLATES]


def template_names() -> list[str]:
    return list(TEMPLATES.keys())


def template_entries() -> list[dict[str, str]]:
    return [get_template_info(name).__dict__ for name in TEMPLATES]


def get_template_info(name: str) -> TemplateInfo:
    template_class = _template_class(name)
    spec = template_class.spec
    return TemplateInfo(route_id=spec.route_id, name=spec.name, title=spec.title, purpose=spec.purpose)


def normalize_template_name(name: str) -> str:
    normalized = str(name or "command-center").strip().lower().replace("_", "-").replace(" ", "-")
    return ROUTE_ALIASES.get(normalized, normalized)
