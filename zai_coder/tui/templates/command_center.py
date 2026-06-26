from .base import BaseTemplate
from .base import TemplatePanel, TemplateSpec

class CommandCenterTemplate(BaseTemplate):
    spec = TemplateSpec(
        route_id="tui-template-01",
        name="command-center",
        title="Command Center",
        purpose="Focus template for chat, command execution, and deep work.",
        status_chips=(
            ("Project", "zai-coder", "active"),
            ("Safe Mode", "local dry-run first", "safe"),
            ("Template", "{template}", "ready"),
            ("Last Command", "{last_command}", "neutral"),
        ),
        panels=(
            TemplatePanel(
                "Header",
                (
                    "Project: zai-coder",
                    "Provider/model: resolved from local CLI config at runtime",
                    "Template: command-center",
                    "Safe mode: external mutation disabled by default",
                ),
            ),
            TemplatePanel(
                "Main Chat / Work Panel",
                (
                    "Operator notes, command output, and deep-work context stay in one focused pane.",
                    "Async refresh updates status without blocking keyboard input.",
                ),
            ),
            TemplatePanel(
                "Right Status Sidebar",
                (
                    "Workspace, dry-run mode, current session, selected template, and last command.",
                    "Status chips use ZeaZ glass-dark contrast without web-only blur effects.",
                ),
            ),
            TemplatePanel("Bottom Command Input", ("Keyboard-first command entry with palette assist.",)),
        ),
        keyboard=("q: quit", "ctrl+k: command palette", "ctrl+r: refresh", "ctrl+d: toggle dry-run mode", "f1: help"),
    )
