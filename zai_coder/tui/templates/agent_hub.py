from .base import BaseTemplate
from .base import TemplatePanel, TemplateSpec

class AgentHubTemplate(BaseTemplate):
    spec = TemplateSpec(
        route_id="tui-template-02",
        name="agent-hub",
        title="Agent Hub",
        purpose="Operator dashboard for monitoring multiple local agents.",
        status_chips=(
            ("Agent Grid", "6 tiles", "active"),
            ("Registry", "{agent_registry}", "ready"),
            ("Skills", "{skill_registry}", "ready"),
            ("Dry Run", "{dry_run}", "dry_run"),
            ("Session", "{session}", "ready"),
        ),
        panels=(
            TemplatePanel("Header", ("Local agent operations overview.", "No remote agent dispatch by default.")),
            TemplatePanel(
                "Tile Grid",
                (
                    "Core Agent - orchestration ready",
                    "Release Agent - release checks ready",
                    "Safety Agent - mutation guard active",
                    "Install Agent - dry-run installer ready",
                    "TUI Agent - template runtime active",
                    "Memory Agent - local state persistence ready",
                ),
            ),
            TemplatePanel("Right Command Panel", ("Doctor, Safety Check, Final Release Status, Install Dry Run.",)),
            TemplatePanel("Bottom Log Panel", ("Rolling local event buffer with secret redaction.",)),
        ),
        keyboard=("q: quit", "tab: cycle focus", "ctrl+k: command palette", "ctrl+r: refresh", "f1: help"),
    )
