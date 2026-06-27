from __future__ import annotations

import json

from .actions import list_palette_commands
from .config import TuiConfig
from .loader import template_entries
from .messages import HELP_TEXT

try:
    from textual.containers import Vertical
    from textual.screen import Screen
    from textual.widgets import Footer, Header, Static
except ImportError:  # pragma: no cover - fallback for environments without Textual

    class Screen:  # type: ignore[too-many-ancestors]
        pass

    class Vertical:  # type: ignore[too-many-ancestors]
        def __init__(self, *children, **kwargs):
            self.children = children
            self.id = kwargs.get("id")
            self.classes = kwargs.get("classes")

    class Header:  # type: ignore[too-many-ancestors]
        def __init__(self, **kwargs):
            self.kwargs = kwargs

    class Footer:  # type: ignore[too-many-ancestors]
        def __init__(self, **kwargs):
            self.kwargs = kwargs

    class Static:  # type: ignore[too-many-ancestors]
        def __init__(self, content: str = "", **kwargs):
            self.id = kwargs.get("id")
            self.content = content
            self.classes = kwargs.get("classes")

        def update(self, text: str) -> None:
            self.content = text


def render_help_screen() -> str:
    return HELP_TEXT + "\n\nCommands:\n" + "\n".join(f"- {item}" for item in list_palette_commands())


def render_config_screen(config: TuiConfig) -> str:
    return "TUI Configuration\n" + json.dumps(config.to_dict(), indent=2, sort_keys=True)


def render_about_screen() -> str:
    return "\n".join(
        [
            "ZAI Coder TUI Command Center",
            "Local-first operator interface for dry-run-safe coding workflows.",
            "Mutation-capable actions remain gated outside this command-center foundation.",
        ]
    )


def render_templates_screen() -> str:
    lines = ["TUI Templates"]
    for entry in template_entries():
        lines.append(f"- {entry['route_id']}: {entry['name']} - {entry['purpose']}")
    return "\n".join(lines)


class HelpScreen(Screen):
    BINDINGS = [("escape", "pop_screen", "Back")]

    def compose(self):
        yield Header()
        yield Vertical(Static(render_help_screen(), classes="panel"))
        yield Footer()

    def action_pop_screen(self):
        self.app.pop_screen()


class ConfigScreen(Screen):
    BINDINGS = [("escape", "pop_screen", "Back")]

    def __init__(self, config: TuiConfig):
        super().__init__()
        self.config = config

    def compose(self):
        yield Header()
        yield Vertical(Static(render_config_screen(self.config), classes="panel"))
        yield Footer()

    def action_pop_screen(self):
        self.app.pop_screen()


class AboutScreen(Screen):
    BINDINGS = [("escape", "pop_screen", "Back")]

    def compose(self):
        yield Header()
        yield Vertical(Static(render_about_screen(), classes="panel"))
        yield Footer()

    def action_pop_screen(self):
        self.app.pop_screen()
