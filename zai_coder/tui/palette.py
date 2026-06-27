from textual.screen import ModalScreen
from textual.widgets import OptionList, Input
from textual.containers import Container
from zai_coder.tui.command_router import list_tui_actions

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
        yield Container(
            OptionList(*[action.name for action in list_tui_actions()], id="palette-options"),
            id="palette-container"
        )

    def on_option_list_option_selected(self, event: OptionList.OptionSelected):
        self.dismiss(event.option.prompt)
