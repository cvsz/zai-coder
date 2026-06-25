"""Quota reservation and commit/release service."""

from __future__ import annotations

import sqlite3
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


SCHEMA = """
CREATE TABLE IF NOT EXISTS quota_reservations (
    id TEXT PRIMARY KEY,
    account_id TEXT NOT NULL,
    workspace_id TEXT NOT NULL,
    resource TEXT NOT NULL,
    amount_units INTEGER NOT NULL,
    status TEXT NOT NULL,
    idempotency_key TEXT NOT NULL UNIQUE,
    created_at TEXT NOT NULL,
    committed_at TEXT,
    released_at TEXT
);
"""


@dataclass
class QuotaReservation:
    id: str
    account_id: str
    workspace_id: str
    resource: str
    amount_units: int
    status: str
    idempotency_key: str
    created_at: str = field(default_factory=now_iso)
    committed_at: str = ""
    released_at: str = ""

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "account_id": self.account_id,
            "workspace_id": self.workspace_id,
            "resource": self.resource,
            "amount_units": self.amount_units,
            "status": self.status,
            "idempotency_key": self.idempotency_key,
            "created_at": self.created_at,
            "committed_at": self.committed_at,
            "released_at": self.released_at,
        }


class QuotaService:
    def __init__(self, db_path: str | Path):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.db_path) as con:
            con.executescript(SCHEMA)

    def reserve(self, account_id: str, workspace_id: str, resource: str, amount_units: int, idempotency_key: str) -> QuotaReservation:
        if amount_units <= 0:
            raise ValueError("amount_units must be positive")
        reservation = QuotaReservation(
            id=str(uuid.uuid4()),
            account_id=account_id,
            workspace_id=workspace_id,
            resource=resource,
            amount_units=amount_units,
            status="reserved",
            idempotency_key=idempotency_key,
        )
        with sqlite3.connect(self.db_path) as con:
            con.execute(
                """
                INSERT INTO quota_reservations
                (id, account_id, workspace_id, resource, amount_units, status, idempotency_key, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    reservation.id,
                    reservation.account_id,
                    reservation.workspace_id,
                    reservation.resource,
                    reservation.amount_units,
                    reservation.status,
                    reservation.idempotency_key,
                    reservation.created_at,
                ),
            )
        return reservation

    def _transition(self, reservation_id: str, expected: str, target: str, time_field: str) -> None:
        timestamp = now_iso()
        with sqlite3.connect(self.db_path) as con:
            cur = con.execute(
                f"UPDATE quota_reservations SET status = ?, {time_field} = ? WHERE id = ? AND status = ?",
                (target, timestamp, reservation_id, expected),
            )
            if cur.rowcount != 1:
                raise ValueError(f"cannot transition reservation {reservation_id} from {expected} to {target}")

    def commit(self, reservation_id: str) -> None:
        self._transition(reservation_id, "reserved", "committed", "committed_at")

    def release(self, reservation_id: str) -> None:
        self._transition(reservation_id, "reserved", "released", "released_at")
