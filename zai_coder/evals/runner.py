from __future__ import annotations

import time
from pathlib import Path

from zai_coder.agents.base import AgentContext
from zai_coder.agents.registry import build_agent
from zai_coder.core.rag import LocalRAG
from zai_coder.core.safety import SafetyPolicy
from zai_coder.core.tools import ToolRuntime

from .cases import EvalCase
from .graders import grade_case


class EvalRunner:
    def __init__(self, workspace: str | Path):
        self.workspace = Path(workspace).expanduser().resolve()

    def _run_agent_case(self, case: EvalCase) -> dict:
        agent = build_agent(case.agent)
        prompt = agent.build_prompt(AgentContext(task=case.prompt, memory=dict(case.memory)))
        return {
            "suite": case.suite,
            "kind": case.kind,
            "agent": case.agent,
            "output": prompt,
            "blocked_reason": "",
            "redacted_output": prompt,
            "ok": True,
            "exit_code": 0,
        }

    def _run_command_case(self, case: EvalCase) -> dict:
        command = case.command or case.prompt
        runtime = ToolRuntime(workspace=self.workspace, safety=SafetyPolicy(), profile=case.profile)
        result = runtime.run(command)
        output = "\n".join(part for part in (result.stdout, result.stderr) if part)
        return {
            "suite": case.suite,
            "kind": case.kind,
            "agent": case.agent,
            "output": output,
            "blocked_reason": result.blocked_reason,
            "redacted_output": output,
            "ok": result.ok,
            "exit_code": result.exit_code,
        }

    def _run_rag_case(self, case: EvalCase) -> dict:
        query = case.query or case.prompt
        rag = LocalRAG(self.workspace)
        output = rag.query(query)
        return {
            "suite": case.suite,
            "kind": case.kind,
            "agent": case.agent,
            "output": output,
            "blocked_reason": "",
            "redacted_output": output,
            "ok": True,
            "exit_code": 0,
        }

    def run_case(self, case: EvalCase) -> dict:
        start = time.time()
        if case.kind == "command" or case.expect_blocked or case.expect_redacted:
            raw = self._run_command_case(case)
        elif case.kind == "rag":
            raw = self._run_rag_case(case)
        else:
            raw = self._run_agent_case(case)

        graded = grade_case(case, raw["output"], blocked_reason=raw["blocked_reason"])
        latency = (time.time() - start) * 1000
        return {
            "id": case.id,
            "suite": case.suite,
            "kind": case.kind,
            "agent": case.agent,
            "passed": graded["passed"],
            "latency_ms": latency,
            "blocked_dangerous_commands": 1 if raw["blocked_reason"] else 0,
            "redaction_success": 1 if graded["redaction_success"] else 0,
            "fallback_model_used": 0,
            "output": raw["output"],
            "blocked_reason": raw["blocked_reason"],
            "checks": graded["checks"],
            "expectations": graded["expectations"],
        }

    def run_suite(self, cases: list[EvalCase]) -> list[dict]:
        return [self.run_case(case) for case in cases]
