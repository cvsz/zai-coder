"""Customer support ticket flow."""

from __future__ import annotations

import sqlite3
import uuid
from pathlib import Path

from .models import SupportTicket


SCHEMA = """
CREATE TABLE IF NOT EXISTS support_tickets (
    id TEXT PRIMARY KEY,
    customer_id TEXT NOT NULL,
    subject TEXT NOT NULL,
    priority TEXT NOT NULL,
    status TEXT NOT NULL,
    category TEXT NOT NULL,
    created_by TEXT NOT NULL,
    created_at TEXT NOT NULL
);
"""


class SupportTicketStore:
    def __init__(self, db_path: str | Path = "data/customer-portal.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.db_path) as con:
            con.executescript(SCHEMA)

    def create_ticket(self, customer_id: str, subject: str, priority: str = "normal", category: str = "general", created_by: str = "customer") -> SupportTicket:
        ticket = SupportTicket(f"ticket_{uuid.uuid4().hex[:12]}", customer_id, subject, priority, "open", category, created_by)
        issues = ticket.validate()
        if issues:
            raise ValueError("; ".join(issues))
        with sqlite3.connect(self.db_path) as con:
            con.execute(
                """
                INSERT INTO support_tickets
                (id, customer_id, subject, priority, status, category, created_by, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (ticket.id, ticket.customer_id, ticket.subject, ticket.priority, ticket.status, ticket.category, ticket.created_by, ticket.created_at),
            )
        return ticket

    def list_tickets(self, customer_id: str | None = None) -> list[dict]:
        with sqlite3.connect(self.db_path) as con:
            if customer_id:
                rows = con.execute(
                    """
                    SELECT id, customer_id, subject, priority, status, category, created_by, created_at
                    FROM support_tickets WHERE customer_id=? ORDER BY created_at DESC
                    """,
                    (customer_id,),
                ).fetchall()
            else:
                rows = con.execute(
                    """
                    SELECT id, customer_id, subject, priority, status, category, created_by, created_at
                    FROM support_tickets ORDER BY created_at DESC
                    """
                ).fetchall()
        return [
            {"id": r[0], "customer_id": r[1], "subject": r[2], "priority": r[3], "status": r[4], "category": r[5], "created_by": r[6], "created_at": r[7]}
            for r in rows
        ]


def support_policy() -> dict:
    return {
        "local_ticket_flow": True,
        "no_external_email_send": True,
        "support_access_requires_approval": True,
        "customer_data_redacted_in_exports": True,
    }
