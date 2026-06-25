from __future__ import annotations


TEXTUAL_MISSING_MESSAGE = """Textual is not installed. Install optional TUI dependencies in a virtual environment:
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[tui]"
"""

HELP_TEXT = """ZAI Coder TUI keyboard help
q: quit
ctrl+k: command palette
ctrl+r: refresh
ctrl+d: toggle dry-run mode
f1: help
"""

COMMAND_PALETTE_TITLE = "ZAI Coder Command Palette"


def render_help(template_name: str, keyboard: list[str]) -> str:
    keys = "\n".join(f"- {item}" for item in keyboard)
    return f"{HELP_TEXT}\nTemplate: {template_name}\nTemplate keys:\n{keys}"
