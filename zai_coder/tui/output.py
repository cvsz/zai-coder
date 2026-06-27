from __future__ import annotations

from .actions import ActionResult
from .safety import redact_secret_text

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


def format_action_result(result: ActionResult) -> str:
    status = "BLOCKED" if result.blocked else ("OK" if result.ok else f"EXIT {result.returncode}")
    lines = [
        f"{result.action_name}: {status}",
        f"command: {' '.join(result.command)}",
    ]
    if result.stdout:
        lines.append(redact_secret_text(result.stdout.rstrip()))
    if result.stderr:
        lines.append(redact_secret_text(result.stderr.rstrip()))
    if result.reason and result.reason not in result.stderr:
        lines.append(f"reason: {redact_secret_text(result.reason)}")
    return "\n".join(lines)


def format_output_panel(items: list[str]) -> str:
    if not items:
        return "Command Output\nNo commands submitted yet."
    return "Command Output\n" + "\n\n".join(redact_secret_text(item) for item in items[-20:])


class OutputPanel(ScrollableContainer):
    """Scrollable command-output panel for Textual with a lightweight fallback."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.content = Static("", id="output-content")
        self.last_output = ""

    def compose(self):
        yield self.content

    def update_output(self, text: str) -> None:
        self.last_output = redact_secret_text(text)
        self.content.update(self.last_output)
