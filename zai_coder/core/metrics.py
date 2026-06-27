import json
import sqlite3
import time
from pathlib import Path
from typing import Dict, Any

class TokenTracker:
    def __init__(self, db_path: str | Path):
        self.db_path = Path(db_path).expanduser().resolve()
        self._init_db()

    def _init_db(self):
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS token_usage (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    model TEXT NOT NULL,
                    prompt_tokens INTEGER NOT NULL,
                    completion_tokens INTEGER NOT NULL,
                    total_tokens INTEGER NOT NULL,
                    timestamp REAL NOT NULL
                )
                """
            )
            conn.commit()

    def record_usage(self, model: str, prompt_tokens: int, completion_tokens: int):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                INSERT INTO token_usage (model, prompt_tokens, completion_tokens, total_tokens, timestamp)
                VALUES (?, ?, ?, ?, ?)
                """,
                (model, prompt_tokens, completion_tokens, prompt_tokens + completion_tokens, time.time())
            )
            conn.commit()
    def get_prometheus_metrics(self) -> str:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.execute("SELECT model, SUM(prompt_tokens) as pt, SUM(completion_tokens) as ct, SUM(total_tokens) as tt FROM token_usage GROUP BY model")
            rows = cur.fetchall()

        lines = [
            "# HELP token_usage_prompt_tokens Total prompt tokens used per model",
            "# TYPE token_usage_prompt_tokens counter",
            "# HELP token_usage_completion_tokens Total completion tokens used per model",
            "# TYPE token_usage_completion_tokens counter",
            "# HELP token_usage_total_tokens Total tokens used per model",
            "# TYPE token_usage_total_tokens counter"
        ]

        for row in rows:
            model = row["model"]
            lines.append(f'token_usage_prompt_tokens{{model="{model}"}} {row["pt"]}')
            lines.append(f'token_usage_completion_tokens{{model="{model}"}} {row["ct"]}')
            lines.append(f'token_usage_total_tokens{{model="{model}"}} {row["tt"]}')
            
        return "\n".join(lines) + "\n"

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

    @staticmethod
    def to_prometheus(metrics: Dict[str, Any]) -> str:
        # Generic fallback for dicts
        lines = []
        for k, v in metrics.items():
            if isinstance(v, (int, float)):
                lines.append(f"# TYPE {k} gauge")
                lines.append(f"{k} {v}")
        return "\n".join(lines) + "\n"
