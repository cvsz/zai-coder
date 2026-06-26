from .base import BaseTemplate
from .base import TemplatePanel, TemplateSpec

class OperationGateTemplate(BaseTemplate):
    spec = TemplateSpec(
        route_id="tui-template-06",
        name="operation-gate",
        title="Operation Gate",
        purpose="Approval-gate and release-gate workflow interface.",
        status_chips=(
            ("Gate", "approval required for apply", "warn"),
            ("Dry Run", "{dry_run}", "dry_run"),
            ("External Mutation", "blocked", "blocked"),
            ("Audit Tail", "{audit_tail}", "neutral"),
            ("Safe Runner", "{safe_command}", "safe"),
            ("Release Status", "{release_status}", "warn"),
        ),
        panels=(
            TemplatePanel(
                "Gate Pipeline",
                (
                    "Plan - command plan and scope",
                    "Dry Run - required evidence before apply",
                    "Review - diff, tests, safety output",
                    "Approval - manual approval only",
                    "Apply - blocked by default in TUI",
                    "Verify - local validation",
                    "Rollback - explicit restore plan",
                ),
            ),
            TemplatePanel("Right Audit Panel", ("Evidence, approval state, and redacted command output.",)),
            TemplatePanel("Bottom Confirmation Panel", ("ctrl+a can approve dry-run result only; it never runs APPLY=1.",)),
        ),
        keyboard=("q: quit", "ctrl+k: command palette", "ctrl+a: approve dry-run result only", "ctrl+r: refresh", "f1: help"),
    )
