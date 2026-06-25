from .base import BaseTemplate
from .base import TemplatePanel, TemplateSpec

class FlowStreamTemplate(BaseTemplate):
    spec = TemplateSpec(
        route_id="tui-template-03",
        name="flow-stream",
        title="Flow Stream",
        purpose="Chronological timeline view for sessions, agent events, commands, and outputs.",
        status_chips=(
            ("Timeline", "live local buffer", "active"),
            ("Filter", "all", "ready"),
            ("Dry Run", "{dry_run}", "dry_run"),
        ),
        panels=(
            TemplatePanel(
                "Vertical Timeline",
                (
                    "Event cards show timestamp, actor, action, status, and summary.",
                    "j/k navigation moves through local event history.",
                ),
            ),
            TemplatePanel("Right Filter Panel", ("all", "commands", "agents", "safety", "errors")),
            TemplatePanel("Bottom Command / Log Input", ("Append local notes or run registered dry-run commands.",)),
        ),
        keyboard=("q: quit", "j/k: move through timeline", "ctrl+f: filter", "ctrl+r: refresh", "f1: help"),
    )
