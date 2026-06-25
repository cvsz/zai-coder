from .base import BaseTemplate
from .base import TemplatePanel, TemplateSpec

class ArchitectTreeTemplate(BaseTemplate):
    spec = TemplateSpec(
        route_id="tui-template-04",
        name="architect-tree",
        title="Architect Tree",
        purpose="Hierarchical tree view for agents, skills, commands, configs, docs, tests, release, and dependencies.",
        status_chips=(
            ("Tree", "architecture map", "active"),
            ("Workspace", "{workspace}", "ready"),
            ("Template", "{template}", "neutral"),
        ),
        panels=(
            TemplatePanel("Left Tree Navigation", ("Agents", "Skills", "Commands", "Config", "Docs", "Tests", "Release")),
            TemplatePanel(
                "Main Detail Panel",
                (
                    "Selected node details, related local commands, and safety notes.",
                    "Dependency and release relationships are represented as inspectable text nodes.",
                ),
            ),
            TemplatePanel("Bottom Status / Action Panel", ("Selected node actions remain dry-run first.",)),
        ),
        keyboard=("q: quit", "arrow keys: navigate tree", "enter: open node", "ctrl+k: command palette", "ctrl+r: refresh", "f1: help"),
    )
