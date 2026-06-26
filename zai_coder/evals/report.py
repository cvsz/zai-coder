import json
from typing import List, Dict

class EvalReporter:
    def __init__(self, results: List[dict]):
        self.results = results
        self.pass_count = sum(1 for r in results if r.get("passed"))
        self.fail_count = len(results) - self.pass_count
        self.blocked = sum(r.get("blocked_dangerous_commands", 0) for r in results)
        self.redactions = sum(r.get("redaction_success", 0) for r in results)
        self.fallbacks = sum(r.get("fallback_model_used", 0) for r in results)
        self.latencies = [r.get("latency_ms", 0) for r in results]
        self.avg_latency = sum(self.latencies) / len(self.latencies) if self.latencies else 0

    def to_json(self) -> str:
        return json.dumps({
            "pass_count": self.pass_count,
            "fail_count": self.fail_count,
            "blocked_dangerous_commands": self.blocked,
            "redaction_success": self.redactions,
            "fallback_model_used": self.fallbacks,
            "avg_latency_ms": self.avg_latency,
            "results": self.results
        }, indent=2)

    def to_markdown(self) -> str:
        md = f"## Evaluation Report\n\n"
        md += f"- **Pass Count**: {self.pass_count}\n"
        md += f"- **Fail Count**: {self.fail_count}\n"
        md += f"- **Blocked Commands**: {self.blocked}\n"
        md += f"- **Redactions**: {self.redactions}\n"
        md += f"- **Fallbacks**: {self.fallbacks}\n"
        md += f"- **Avg Latency**: {self.avg_latency:.2f} ms\n"
        return md
