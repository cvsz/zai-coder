from __future__ import annotations

from .navigation import command_palette_entries

try:
    from textual.containers import Container
    from textual.screen import ModalScreen
    from textual.widgets import OptionList
except ImportError:  # pragma: no cover - fallback for environments without Textual
    class ModalScreen:  # type: ignore[too-many-ancestors]
        def __init__(self, *args, **kwargs):
            self.args = args
            self.kwargs = kwargs

        def dismiss(self, value=None):
            self.value = value

    class Container:  # type: ignore[too-many-ancestors]
        def __init__(self, *children, **kwargs):
            self.children = children
            self.id = kwargs.get("id")

    class OptionList:  # type: ignore[too-many-ancestors]
        class OptionSelected:
            def __init__(self, option):
                self.option = option

        def __init__(self, *options, **kwargs):
            self.options = list(options)
            self.id = kwargs.get("id")

        def focus(self):
            return None


class CommandPalette(ModalScreen):
    CSS = """
    CommandPalette {
        align: center middle;
    }
    #palette-container {
        width: 60;
        height: auto;
        border: round #77d7c8;
        background: #0d1b24;
    }
    """

    def compose(self):
        entries = command_palette_entries()
        yield Container(
            OptionList(*[entry.label for entry in entries], id="palette-options"),
            id="palette-container",
        )

    def on_mount(self) -> None:
        palette = getattr(self, "query_one", None)
        if callable(palette):
            try:
                self.query_one("#palette-options", OptionList).focus()
            except Exception:
                pass

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        option = getattr(event, "option", None)
        prompt = getattr(option, "prompt", None) or getattr(option, "label", None) or str(option)
        self.dismiss(prompt)
