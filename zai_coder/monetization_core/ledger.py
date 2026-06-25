"""Append-only credit ledger.

Use integer credit units only. No floating point money here.
"""

from __future__ import annotations

import sqlite3
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import List


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


LEDGER_SCHEMA = """
CREATE TABLE IF NOT EXISTS credit_ledger_entries (
    id TEXT PRIMARY KEY,
    account_id TEXT NOT NULL,
    workspace_id TEXT NOT NULL,
    type TEXT NOT NULL,
    amount_units INTEGER NOT NULL,
    reason TEXT NOT NULL,
    idempotency_key TEXT NOT NULL UNIQUE,
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL
);
"""


@dataclass(frozen=True)
class CreditLedgerEntry:
    id: str
    account_id: str
    workspace_id: str
    type: str
    amount_units: int
    reason: str
    idempotency_key: str
    metadata_json: str = "{}"
    created_at: str = field(default_factory=now_iso)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "account_id": self.account_id,
            "workspace_id": self.workspace_id,
            "type": self.type,
            "amount_units": self.amount_units,
            "reason": self.reason,
            "idempotency_key": self.idempotency_key,
            "metadata_json": self.metadata_json,
            "created_at": self.created_at,
        }


class CreditLedger:
    def __init__(self, db_path: str | Path):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.db_path) as con:
            con.executescript(LEDGER_SCHEMA)

    def append(
        self,
        account_id: str,
        workspace_id: str,
        entry_type: str,
        amount_units: int,
        reason: str,
        idempotency_key: str,
        metadata_json: str = "{}",
    ) -> CreditLedgerEntry:
        if amount_units == 0:
            raise ValueError("amount_units must be non-zero")
        if entry_type not in {"grant", "debit", "refund", "adjustment", "expire"}:
            raise ValueError(f"invalid ledger entry type: {entry_type}")

        entry = CreditLedgerEntry(
            id=str(uuid.uuid4()),
            account_id=account_id,
            workspace_id=workspace_id,
            type=entry_type,
            amount_units=int(amount_units),
            reason=reason,
            idempotency_key=idempotency_key,
            metadata_json=metadata_json,
        )

        with sqlite3.connect(self.db_path) as con:
            con.execute(
                """
                INSERT INTO credit_ledger_entries
                (id, account_id, workspace_id, type, amount_units, reason, idempotency_key, metadata_json, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    entry.id,
                    entry.account_id,
                    entry.workspace_id,
                    entry.type,
                    entry.amount_units,
                    entry.reason,
                    entry.idempotency_key,
                    entry.metadata_json,
                    entry.created_at,
                ),
            )
        return entry

    def balance(self, account_id: str, workspace_id: str = "") -> int:
        query = "SELECT COALESCE(SUM(amount_units), 0) FROM credit_ledger_entries WHERE account_id = ?"
        params: list[object] = [account_id]
        if workspace_id:
            query += " AND workspace_id = ?"
            params.append(workspace_id)
        with sqlite3.connect(self.db_path) as con:
            value = con.execute(query, params).fetchone()[0]
        return int(value)

    def list_entries(self, account_id: str) -> List[CreditLedgerEntry]:
        with sqlite3.connect(self.db_path) as con:
            rows = con.execute(
                """
                SELECT id, account_id, workspace_id, type, amount_units, reason, idempotency_key, metadata_json, created_at
                FROM credit_ledger_entries
                WHERE account_id = ?
                ORDER BY created_at ASC
                """,
                (account_id,),
            ).fetchall()
        return [
            CreditLedgerEntry(
                id=row[0],
                account_id=row[1],
                workspace_id=row[2],
                type=row[3],
                amount_units=row[4],
                reason=row[5],
                idempotency_key=row[6],
                metadata_json=row[7],
                created_at=row[8],
            )
            for row in rows
        ]
