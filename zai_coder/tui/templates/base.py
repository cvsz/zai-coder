from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from ..actions import list_palette_commands
from ..design_tokens import render_chip
from ..state import TuiState


@dataclass(frozen=True)
class TemplatePanel:
    title: str
    lines: tuple[str, ...]


@dataclass(frozen=True)
class TemplateSpec:
    route_id: str
    name: str
    title: str
    purpose: str
    keyboard: tuple[str, ...]
    panels: tuple[TemplatePanel, ...]
    status_chips: tuple[tuple[str, str, str], ...] = field(default_factory=tuple)


class BaseTemplate:
    spec: TemplateSpec

    def __init__(self, state: TuiState | None = None) -> None:
        self.state = state or TuiState()

    @property
    def route_id(self) -> str:
        return self.spec.route_id

    @property
    def name(self) -> str:
        return self.spec.name

    @property
    def purpose(self) -> str:
        return self.spec.purpose

    @property
    def keyboard(self) -> list[str]:
        return list(self.spec.keyboard)

    def as_dict(self) -> dict[str, Any]:
        return {
            "route_id": self.route_id,
            "name": self.name,
            "title": self.spec.title,
            "purpose": self.purpose,
            "keyboard": self.keyboard,
            "panels": [{"title": panel.title, "lines": list(panel.lines)} for panel in self.spec.panels],
        }

    def render(self) -> str:
        return self.render_static()

    def render_static(self) -> str:
        chips = [
            render_chip(label, self._resolve_chip_value(value), tone)
            for label, value, tone in self.spec.status_chips
        ]
        header = [
            f"ZAI Coder TUI - {self.spec.title}",
            f"route={self.route_id} template={self.name}",
            f"purpose={self.purpose}",
            " ".join(chips),
        ]
        panels = []
        for panel in self.spec.panels:
            panel_lines = "\n".join(f"  {line}" for line in panel.lines)
            panels.append(f"+ {panel.title}\n{panel_lines}")
        palette = "\n".join(f"  - {item}" for item in list_palette_commands())
        keys = "\n".join(f"  - {item}" for item in self.keyboard)
        return "\n\n".join(
            [
                "\n".join(header),
                "\n\n".join(panels),
                "+ Command Palette\n" + palette,
                "+ Keyboard\n" + keys,
            ]
        )

    def _resolve_chip_value(self, value: str) -> str:
        if value == "{dry_run}":
            return "on" if self.state.dry_run_mode else "off"
        if value == "{template}":
            return self.state.active_template
        if value == "{session}":
            return self.state.current_session
        if value == "{workspace}":
            return self.state.workspace
        if value == "{last_command}":
            return self.state.last_command or "none"
        return value
