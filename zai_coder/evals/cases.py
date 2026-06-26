import json
from pathlib import Path
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class EvalCase:
    id: str
    prompt: str
    expect_blocked: bool = False
    expect_redacted: bool = False
    expect_substring: Optional[str] = None
    agent: Optional[str] = None

class CaseLoader:
    def __init__(self, workspace: str | Path):
        self.assets_dir = Path(workspace) / "assets" / "evals"

    def load_suite(self, suite_name: str) -> List[EvalCase]:
        path = self.assets_dir / f"{suite_name}.json"
        if not path.exists():
            return []
            
        data = json.loads(path.read_text(encoding="utf-8"))
        cases = []
        for c in data:
            cases.append(EvalCase(
                id=c.get("id", ""),
                prompt=c.get("prompt", ""),
                expect_blocked=c.get("expect_blocked", False),
                expect_redacted=c.get("expect_redacted", False),
                expect_substring=c.get("expect_substring"),
                agent=c.get("agent")
            ))
        return cases
