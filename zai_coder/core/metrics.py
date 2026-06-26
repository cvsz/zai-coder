import json
from typing import Dict, Any

class MetricsFormatter:
    @staticmethod
    def to_json(metrics: Dict[str, Any]) -> str:
        return json.dumps(metrics, indent=2)

    @staticmethod
    def to_markdown(metrics: Dict[str, Any]) -> str:
        lines = [
            "| Metric | Value |",
            "|---|---|"
        ]
        
        for k, v in metrics.items():
            if isinstance(v, dict):
                v_str = ", ".join(f"{dk}: {dv}" for dk, dv in v.items())
            else:
                v_str = str(v)
            name = k.replace("_", " ").title()
            lines.append(f"| {name} | {v_str} |")
            
        return "\n".join(lines)
