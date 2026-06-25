"""AI workflow builder."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


ALLOWED_STEP_TYPES = {"agent", "skill", "integration_plan", "approval", "notify", "deploy_plan"}


@dataclass(frozen=True)
class WorkflowStep:
    name: str
    step_type: str
    config: dict = field(default_factory=dict)

    def validate(self) -> list[str]:
        issues = []
        if not self.name:
            issues.append("missing step name")
        if self.step_type not in ALLOWED_STEP_TYPES:
            issues.append(f"invalid step_type: {self.step_type}")
        return issues

    def to_dict(self) -> dict:
        return {"name": self.name, "step_type": self.step_type, "config": dict(self.config)}


@dataclass(frozen=True)
class Workflow:
    slug: str
    name: str
    steps: List[WorkflowStep]
    status: str = "draft"

    def validate(self) -> list[str]:
        issues = []
        if not self.slug:
            issues.append("missing slug")
        if not self.name:
            issues.append("missing name")
        if self.status not in {"draft", "review", "approved", "active", "archived"}:
            issues.append(f"invalid status: {self.status}")
        if not self.steps:
            issues.append("workflow requires at least one step")
        for step in self.steps:
            issues.extend(step.validate())
        return issues

    def to_dict(self) -> dict:
        return {"slug": self.slug, "name": self.name, "steps": [s.to_dict() for s in self.steps], "status": self.status}


def default_release_workflow() -> Workflow:
    return Workflow(
        slug="safe-release",
        name="Safe Release Workflow",
        steps=[
            WorkflowStep("Run tests", "skill", {"command": "python3 -m pytest -q"}),
            WorkflowStep("Safety scan", "skill", {"command": "make scan"}),
            WorkflowStep("Build release plan", "deploy_plan", {"target": "release"}),
            WorkflowStep("Human approval", "approval", {"required": True}),
            WorkflowStep("Notification draft", "notify", {"channel": "ops"}),
        ],
    )
