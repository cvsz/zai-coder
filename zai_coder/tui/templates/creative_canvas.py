from .base import BaseTemplate
from .base import TemplatePanel, TemplateSpec

class CreativeCanvasTemplate(BaseTemplate):
    spec = TemplateSpec(
        route_id="tui-template-05",
        name="creative-canvas",
        title="Creative Canvas",
        purpose="Media and preview-heavy template for creative, docs, prompts, screenshots, and generated artifacts.",
        status_chips=(
            ("Preview", "text/file/media panes", "active"),
            ("Safe Mode", "local preview only", "safe"),
            ("Dry Run", "{dry_run}", "dry_run"),
        ),
        panels=(
            TemplatePanel("Left Prompt / Session Panel", ("Prompt notes, docs tasks, and generation context.",)),
            TemplatePanel(
                "Center Preview Canvas",
                (
                    "Text preview area",
                    "File preview pane for selected local artifacts",
                    "Media preview pane for screenshots and generated artifacts",
                ),
            ),
            TemplatePanel("Right Metadata / Status Panel", ("Artifact path, safety mode, and latest local command.",)),
            TemplatePanel("Bottom Command Input", ("Preview-focused commands only; no external upload.",)),
        ),
        keyboard=("q: quit", "ctrl+p: preview panel focus", "ctrl+k: command palette", "ctrl+r: refresh", "f1: help"),
    )
