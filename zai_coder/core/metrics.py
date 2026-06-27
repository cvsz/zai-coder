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
