from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .runner import AgentRunner, RunnerModel


@dataclass
class SubagentConfig:
    agent_name: str
    task: str
    toolset: list[str] = field(default_factory=list)
    isolated_context: bool = True
    shared_state: bool = False

@dataclass
class DelegationPlan:
    task: str
    subagents: list[SubagentConfig]
    max_subagents: int = 3
    
    def validate(self):
        if len(self.subagents) > self.max_subagents:
            raise ValueError(f"Exceeded max subagents: {len(self.subagents)} > {self.max_subagents}")
        for sa in self.subagents:
            if sa.shared_state:
                raise ValueError("Shared mutable state is not allowed by default")

class DelegationOrchestrator:
    def __init__(self, workspace: str | Path):
        self.workspace = Path(workspace).expanduser().resolve()
        self.runner = AgentRunner(self.workspace)

    def plan_delegation(self, parent_task: str, subagent_tasks: list[dict[str, str]]) -> DelegationPlan:
        configs = []
        for st in subagent_tasks:
            configs.append(SubagentConfig(
                agent_name=st["agent_name"],
                task=st["task"],
                toolset=["safe_runner_restricted"] # Restricted by default
            ))
        
        plan = DelegationPlan(task=parent_task, subagents=configs)
        plan.validate()
        return plan

    def execute_plan_dry_run(self, plan: DelegationPlan, parent_run_id: str | None = None) -> list[RunnerModel]:
        results = []
        for config in plan.subagents:
            run = self.runner.create_run(
                task=config.task,
                agent_name=config.agent_name,
                parent_run_id=parent_run_id
            )
            # Parent collects child summaries only (redacted child output logic placeholder)
            result = self.runner.execute_dry_run(run)
            result.summary = f"[REDACTED_FOR_PARENT] {result.summary}"
            results.append(result)
        return results
