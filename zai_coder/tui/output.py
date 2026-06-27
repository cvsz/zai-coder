from __future__ import annotations

try:
    from textual.containers import ScrollableContainer
    from textual.widgets import Static
except ImportError:  # pragma: no cover - fallback for environments without Textual
    class ScrollableContainer:  # type: ignore[too-many-ancestors]
        def __init__(self, **kwargs):
            self.id = kwargs.get("id")
            self.classes = kwargs.get("classes")

    class Static:  # type: ignore[too-many-ancestors]
        def __init__(self, content: str = "", **kwargs):
            self.id = kwargs.get("id")
            self.content = content

        def update(self, text: str) -> None:
            self.content = text


class OutputPanel(ScrollableContainer):
    """Panel to display command output and logs."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.content = Static("", id="output-content")
        self.last_output = ""

    def compose(self):
        yield self.content

    def update_output(self, text: str):
        self.last_output = text
        self.content.update(text)
