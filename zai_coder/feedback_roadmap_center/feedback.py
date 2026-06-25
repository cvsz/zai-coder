"""Feedback inbox and triage."""

from __future__ import annotations

import sqlite3
import uuid
from pathlib import Path

from .models import FeedbackItem


SCHEMA = """
CREATE TABLE IF NOT EXISTS feedback_items (
    id TEXT PRIMARY KEY,
    customer_id TEXT NOT NULL,
    title TEXT NOT NULL,
    body TEXT NOT NULL,
    category TEXT NOT NULL,
    sentiment TEXT NOT NULL,
    priority_hint TEXT NOT NULL,
    status TEXT NOT NULL,
    source TEXT NOT NULL,
    created_at TEXT NOT NULL
);
"""


class FeedbackInbox:
    def __init__(self, db_path: str | Path = "data/feedback-roadmap.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.db_path) as con:
            con.executescript(SCHEMA)

    def submit_feedback(
        self,
        customer_id: str,
        title: str,
        body: str,
        category: str = "feature",
        sentiment: str = "neutral",
        priority_hint: str = "normal",
        source: str = "portal",
    ) -> FeedbackItem:
        item = FeedbackItem(f"fb_{uuid.uuid4().hex[:12]}", customer_id, title, body, category, sentiment, priority_hint, "new", source)
        issues = item.validate()
        if issues:
            raise ValueError("; ".join(issues))
        with sqlite3.connect(self.db_path) as con:
            con.execute(
                """
                INSERT INTO feedback_items
                (id, customer_id, title, body, category, sentiment, priority_hint, status, source, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (item.id, item.customer_id, item.title, item.body, item.category, item.sentiment, item.priority_hint, item.status, item.source, item.created_at),
            )
        return item

    def list_feedback(self, customer_id: str | None = None) -> list[dict]:
        with sqlite3.connect(self.db_path) as con:
            if customer_id:
                rows = con.execute(
                    """
                    SELECT id, customer_id, title, body, category, sentiment, priority_hint, status, source, created_at
                    FROM feedback_items WHERE customer_id=? ORDER BY created_at DESC
                    """,
                    (customer_id,),
                ).fetchall()
            else:
                rows = con.execute(
                    """
                    SELECT id, customer_id, title, body, category, sentiment, priority_hint, status, source, created_at
                    FROM feedback_items ORDER BY created_at DESC
                    """
                ).fetchall()
        return [
            {
                "id": r[0],
                "customer_id": r[1],
                "title": r[2],
                "body": r[3],
                "category": r[4],
                "sentiment": r[5],
                "priority_hint": r[6],
                "status": r[7],
                "source": r[8],
                "created_at": r[9],
            }
            for r in rows
        ]


def feedback_triage(item: dict) -> dict:
    score = 1
    if item["priority_hint"] == "urgent":
        score += 5
    elif item["priority_hint"] == "high":
        score += 3
    elif item["priority_hint"] == "normal":
        score += 1
    if item["sentiment"] == "negative":
        score += 2
    if item["category"] in {"bug", "billing", "compliance"}:
        score += 2
    queue = "critical_review" if score >= 7 else "product_review" if score >= 4 else "backlog"
    return {"feedback_id": item["id"], "score": score, "queue": queue, "status": "triaged"}


def seed_demo_feedback(db_path: str | Path = "data/feedback-roadmap.db") -> list[dict]:
    inbox = FeedbackInbox(db_path)
    rows = [
        inbox.submit_feedback("cust_demo", "Need GitHub connector setup wizard", "Make connector setup easier.", "integration", "neutral", "high"),
        inbox.submit_feedback("cust_demo", "Onboarding checklist is helpful", "Keep the welcome checklist visible.", "docs", "positive", "normal"),
        inbox.submit_feedback("cust_local", "Need enterprise roadmap export", "Board reporting should include roadmap status.", "feature", "neutral", "high"),
        inbox.submit_feedback("cust_demo", "Billing upgrade flow should be clearer", "Explain draft-only billing and sandbox payment steps.", "billing", "negative", "normal"),
    ]
    return [row.to_dict() for row in rows]
