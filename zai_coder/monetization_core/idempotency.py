"""Idempotency key store for billing and quota operations."""

from __future__ import annotations

import hashlib
import sqlite3
from datetime import datetime, timezone
from pathlib import Path


SCHEMA = """
CREATE TABLE IF NOT EXISTS idempotency_keys (
    key TEXT PRIMARY KEY,
    operation TEXT NOT NULL,
    request_hash TEXT NOT NULL,
    response_json TEXT NOT NULL,
    status TEXT NOT NULL,
    created_at TEXT NOT NULL
);
"""


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def hash_payload(payload: str) -> str:
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


class IdempotencyStore:
    def __init__(self, db_path: str | Path):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.db_path) as con:
            con.executescript(SCHEMA)

    def exists(self, key: str) -> bool:
        with sqlite3.connect(self.db_path) as con:
            row = con.execute("SELECT key FROM idempotency_keys WHERE key = ?", (key,)).fetchone()
        return row is not None

    def record(self, key: str, operation: str, request_payload: str, response_json: str, status: str = "completed") -> None:
        if status not in {"started", "completed", "failed"}:
            raise ValueError(f"invalid idempotency status: {status}")
        with sqlite3.connect(self.db_path) as con:
            con.execute(
                """
                INSERT INTO idempotency_keys
                (key, operation, request_hash, response_json, status, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (key, operation, hash_payload(request_payload), response_json, status, now_iso()),
            )
