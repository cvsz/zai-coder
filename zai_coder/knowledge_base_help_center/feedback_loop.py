"""Article feedback loop."""

from __future__ import annotations

import sqlite3
import uuid
from pathlib import Path

from .models import HelpFeedback


SCHEMA = """
CREATE TABLE IF NOT EXISTS help_feedback (
    id TEXT PRIMARY KEY,
    article_id TEXT NOT NULL,
    helpful INTEGER NOT NULL,
    comment TEXT NOT NULL,
    customer_id TEXT NOT NULL,
    created_at TEXT NOT NULL
);
"""


class HelpFeedbackStore:
    def __init__(self, db_path: str | Path = "data/help-center.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.db_path) as con:
            con.executescript(SCHEMA)

    def submit(self, article_id: str, helpful: bool, comment: str = "", customer_id: str = "anonymous") -> HelpFeedback:
        item = HelpFeedback(f"hf_{uuid.uuid4().hex[:12]}", article_id, helpful, comment, customer_id)
        issues = item.validate()
        if issues:
            raise ValueError("; ".join(issues))
        with sqlite3.connect(self.db_path) as con:
            con.execute(
                """
                INSERT INTO help_feedback
                (id, article_id, helpful, comment, customer_id, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (item.id, item.article_id, int(item.helpful), item.comment, item.customer_id, item.created_at),
            )
        return item

    def list_feedback(self, article_id: str | None = None) -> list[dict]:
        with sqlite3.connect(self.db_path) as con:
            if article_id:
                rows = con.execute(
                    """
                    SELECT id, article_id, helpful, comment, customer_id, created_at
                    FROM help_feedback WHERE article_id=? ORDER BY created_at DESC
                    """,
                    (article_id,),
                ).fetchall()
            else:
                rows = con.execute(
                    """
                    SELECT id, article_id, helpful, comment, customer_id, created_at
                    FROM help_feedback ORDER BY created_at DESC
                    """
                ).fetchall()
        return [
            {"id": r[0], "article_id": r[1], "helpful": bool(r[2]), "comment": r[3], "customer_id": r[4], "created_at": r[5]}
            for r in rows
        ]


def article_feedback_summary(rows: list[dict]) -> dict:
    total = len(rows)
    helpful = sum(1 for row in rows if row["helpful"])
    return {
        "total": total,
        "helpful": helpful,
        "not_helpful": total - helpful,
        "helpful_rate": 0.0 if total == 0 else round(helpful / total, 4),
        "needs_review": total > 0 and helpful / total < 0.7,
    }
