from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

@dataclass
class RunnerModel:
    run_id: str
    task: str
    agent_name: str
    workspace: str
    profile: str = "default"
    parent_run_id: str | None = None
    status: str = "pending" # pending, running, blocked, completed, failed
    max_steps: int = 50
    timeout_seconds: int = 3600
    created_at: float = field(default_factory=time.time)
    completed_at: float | None = None
    summary: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "run_id": self.run_id,
            "parent_run_id": self.parent_run_id,
            "task": self.task,
            "agent_name": self.agent_name,
            "profile": self.profile,
            "workspace": self.workspace,
            "status": self.status,
            "max_steps": self.max_steps,
            "timeout_seconds": self.timeout_seconds,
            "created_at": self.created_at,
            "completed_at": self.completed_at,
            "summary": self.summary
        }

class AgentRunner:
    def __init__(self, workspace: str | Path):
        self.workspace = str(Path(workspace).expanduser().resolve())

    def create_run(self, task: str, agent_name: str, parent_run_id: str | None = None) -> RunnerModel:
        return RunnerModel(
            run_id=str(uuid.uuid4()),
            task=task,
            agent_name=agent_name,
            workspace=self.workspace,
            parent_run_id=parent_run_id
        )

    def execute_dry_run(self, run: RunnerModel) -> RunnerModel:
        """Simulate a deterministic, sequential execution."""
        run.status = "running"
        
        # Simulate execution
        # In this dry-run foundation, we just return simulated completion.
        
        run.status = "completed"
        run.completed_at = time.time()
        run.summary = f"[DRY-RUN] Executed task '{run.task[:20]}...' using agent '{run.agent_name}'"
        return run
