"""Local API key management for ZAI App Studio.

Raw API keys are returned only at creation time. Storage uses salted SHA-256
hashing to avoid plaintext key storage.
"""

from __future__ import annotations

import hashlib
import secrets
import sqlite3
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


SCHEMA = """
CREATE TABLE IF NOT EXISTS api_keys (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    prefix TEXT NOT NULL,
    salt TEXT NOT NULL,
    key_hash TEXT NOT NULL,
    status TEXT NOT NULL,
    created_at TEXT NOT NULL,
    revoked_at TEXT
);
"""


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def hash_key(raw_key: str, salt: str) -> str:
    return hashlib.sha256((salt + ":" + raw_key).encode("utf-8")).hexdigest()


@dataclass
class ApiKeyRecord:
    id: str
    name: str
    prefix: str
    status: str = "active"
    created_at: str = field(default_factory=now_iso)
    revoked_at: str = ""

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "prefix": self.prefix,
            "status": self.status,
            "created_at": self.created_at,
            "revoked_at": self.revoked_at,
        }


class ApiKeyManager:
    def __init__(self, db_path: str | Path):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.db_path) as con:
            con.executescript(SCHEMA)

    def create_key(self, name: str) -> tuple[ApiKeyRecord, str]:
        if not name.strip():
            raise ValueError("missing API key name")
        raw_key = "zai_" + secrets.token_urlsafe(32)
        prefix = raw_key[:12]
        salt = secrets.token_hex(16)
        record = ApiKeyRecord(id=str(uuid.uuid4()), name=name.strip(), prefix=prefix)
        with sqlite3.connect(self.db_path) as con:
            con.execute(
                """
                INSERT INTO api_keys
                (id, name, prefix, salt, key_hash, status, created_at, revoked_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    record.id,
                    record.name,
                    record.prefix,
                    salt,
                    hash_key(raw_key, salt),
                    record.status,
                    record.created_at,
                    record.revoked_at,
                ),
            )
        return record, raw_key

    def verify_key(self, raw_key: str) -> Optional[ApiKeyRecord]:
        if not raw_key:
            return None
        prefix = raw_key[:12]
        with sqlite3.connect(self.db_path) as con:
            row = con.execute(
                """
                SELECT id, name, prefix, salt, key_hash, status, created_at, COALESCE(revoked_at, '')
                FROM api_keys
                WHERE prefix = ?
                """,
                (prefix,),
            ).fetchone()
        if not row:
            return None
        if row[5] != "active":
            return None
        if hash_key(raw_key, row[3]) != row[4]:
            return None
        return ApiKeyRecord(id=row[0], name=row[1], prefix=row[2], status=row[5], created_at=row[6], revoked_at=row[7])

    def revoke_key(self, key_id: str) -> None:
        with sqlite3.connect(self.db_path) as con:
            cur = con.execute(
                "UPDATE api_keys SET status = 'revoked', revoked_at = ? WHERE id = ? AND status = 'active'",
                (now_iso(), key_id),
            )
            if cur.rowcount != 1:
                raise KeyError(f"active API key not found: {key_id}")

    def list_keys(self) -> list[ApiKeyRecord]:
        with sqlite3.connect(self.db_path) as con:
            rows = con.execute(
                "SELECT id, name, prefix, status, created_at, COALESCE(revoked_at, '') FROM api_keys ORDER BY created_at"
            ).fetchall()
        return [
            ApiKeyRecord(id=row[0], name=row[1], prefix=row[2], status=row[3], created_at=row[4], revoked_at=row[5])
            for row in rows
        ]
