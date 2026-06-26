from __future__ import annotations

from dataclasses import dataclass

from .actions import PALETTE_COMMANDS
from .loader import normalize_template_name, template_names


@dataclass(frozen=True)
class CommandPaletteEntry:
    id: str
    label: str
    kind: str
    target: str = ""


KEYBOARD_BINDINGS = {
    "common": ["q", "ctrl+k", "ctrl+r", "f1"],
    "command-center": ["q", "ctrl+k", "ctrl+r", "ctrl+d", "f1"],
    "agent-hub": ["q", "tab", "ctrl+k", "ctrl+r", "f1"],
    "flow-stream": ["q", "j", "k", "ctrl+f", "ctrl+r", "f1"],
    "architect-tree": ["q", "up", "down", "left", "right", "enter", "ctrl+k", "ctrl+r", "f1"],
    "creative-canvas": ["q", "ctrl+p", "ctrl+k", "ctrl+r", "f1"],
    "operation-gate": ["q", "ctrl+k", "ctrl+a", "ctrl+r", "f1"],
}


def command_palette_entries() -> list[CommandPaletteEntry]:
    entries = [
        CommandPaletteEntry(item.lower().replace(": ", "-").replace(" ", "-"), item, "command")
        for item in PALETTE_COMMANDS
        if not item.startswith("Switch:")
    ]
    entries.extend(
        CommandPaletteEntry(f"switch-{name}", f"Switch: {name.replace('-', ' ').title()}", "template-switch", name)
        for name in template_names()
    )
    return entries


def help_entries(template_name: str) -> list[str]:
    return KEYBOARD_BINDINGS.get(normalize_template_name(template_name), KEYBOARD_BINDINGS["common"])


@dataclass
class TemplateNavigator:
    active_template: str = "command-center"

    def switch(self, template_name: str) -> str:
        normalized = normalize_template_name(template_name)
        if normalized not in template_names():
            available = ", ".join(template_names())
            raise ValueError(f"Cannot switch to unknown template '{template_name}'. Available: {available}")
        self.active_template = normalized
        return self.active_template

    def next_template(self) -> str:
        templates = template_names()
        index = templates.index(self.active_template) if self.active_template in templates else 0
        self.active_template = templates[(index + 1) % len(templates)]
        return self.active_template
