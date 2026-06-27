from __future__ import annotations

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


class HelpScreen(Screen):
    """Screen to display help information."""

    BINDINGS = [("escape", "pop_screen", "Back")]

    def compose(self):
        yield Header()
        yield Vertical(
            Static("ZAI Coder TUI Command Center Help", classes="panel"),
            Static("Use ctrl+k for palette, ctrl+r to refresh, q to quit.", classes="panel"),
        )
        yield Footer()

    def action_pop_screen(self):
        self.app.pop_screen()
