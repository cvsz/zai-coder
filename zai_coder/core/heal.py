from pathlib import Path
from .failure_parser import FailureParser
import json

class SelfHeal:
    def __init__(self, workspace: str | Path):
        self.workspace = Path(workspace).resolve()
        self.parser = FailureParser()

    def analyze_log(self, log_text: str) -> list[dict]:
        return self.parser.parse(log_text)

    def generate_plan(self, failures: list[dict]) -> str:
        if not failures:
            return "No failures detected."
            
        plan = "### Repair Plan\n\n"
        for i, f in enumerate(failures, 1):
            plan += f"{i}. Type: {f.get('type')}\n"
            if "file" in f:
                plan += f"   File: {f['file']}\n"
            if "error" in f:
                plan += f"   Error: {f['error']}\n"
            plan += "\n"
            
        plan += "\nRun the LLM agent to generate a fix diff for these failures."
        return plan
