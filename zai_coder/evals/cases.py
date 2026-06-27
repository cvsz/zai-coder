from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class EvalCase:
    id: str
    prompt: str
    suite: str = ""
    kind: str = "agent"
    agent: str = "planner"
    command: str = ""
    query: str = ""
    profile: str = "operator"
    expect_blocked: bool = False
    expect_redacted: bool = False
    expect_substring: str | None = None
    expect_contains: tuple[str, ...] = ()
    expect_not_contains: tuple[str, ...] = ()
    memory: dict[str, Any] = field(default_factory=dict)


class CaseLoader:
    def __init__(self, workspace: str | Path):
        self.workspace = Path(workspace)
        self.roots = [self.workspace / "assets" / "evals", self.workspace / "evals"]

    def _load_payload(self, path: Path) -> list[dict[str, Any]]:
        if path.suffix == ".jsonl":
            payload: list[dict[str, Any]] = []
            for line in path.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if line:
                    payload.append(json.loads(line))
            return payload
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            return [data]
        return list(data)

    def _record_to_case(self, payload: dict[str, Any], suite_name: str) -> EvalCase:
        expect_contains = payload.get("expect_contains") or []
        expect_not_contains = payload.get("expect_not_contains") or []
        memory = payload.get("memory") or {}
        return EvalCase(
            id=str(payload.get("id", "")),
            prompt=str(payload.get("prompt", "")),
            suite=str(payload.get("suite", suite_name)),
            kind=str(payload.get("kind", "agent")),
            agent=str(payload.get("agent", "planner")),
            command=str(payload.get("command", "")),
            query=str(payload.get("query", "")),
            profile=str(payload.get("profile", "operator")),
            expect_blocked=bool(payload.get("expect_blocked", False)),
            expect_redacted=bool(payload.get("expect_redacted", False)),
            expect_substring=payload.get("expect_substring"),
            expect_contains=tuple(str(item) for item in expect_contains),
            expect_not_contains=tuple(str(item) for item in expect_not_contains),
            memory=dict(memory),
        )

    def _load_file(self, path: Path, suite_name: str) -> list[EvalCase]:
        return [self._record_to_case(payload, suite_name) for payload in self._load_payload(path)]

    def load_suite(self, suite_name: str) -> list[EvalCase]:
        cases: list[EvalCase] = []
        for root in self.roots:
            for suffix in (".jsonl", ".json"):
                path = root / f"{suite_name}{suffix}"
                if path.exists():
                    cases.extend(self._load_file(path, suite_name))
            cases_file = root / "cases.jsonl"
            if cases_file.exists():
                for case in self._load_file(cases_file, suite_name=""):
                    if case.suite == suite_name:
                        cases.append(case)
        return cases

    def available_suites(self) -> list[str]:
        suites: set[str] = set()
        for root in self.roots:
            for path in root.glob("*.json*"):
                if path.name == "cases.jsonl":
                    for case in self._load_file(path, suite_name=""):
                        if case.suite:
                            suites.add(case.suite)
                    continue
                for case in self._load_file(path, suite_name=path.stem):
                    suites.add(case.suite or path.stem)
        return sorted(suites)
