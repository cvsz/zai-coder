"""SQLite-backed session store.

Tokens are stored as salted hashes. Raw tokens are only returned once.
"""

from __future__ import annotations

import hashlib
import secrets
import sqlite3
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path


SCHEMA = """
CREATE TABLE IF NOT EXISTS sessions (
    id TEXT PRIMARY KEY,
    actor TEXT NOT NULL,
    token_prefix TEXT NOT NULL,
    salt TEXT NOT NULL,
    token_hash TEXT NOT NULL,
    scopes_csv TEXT NOT NULL,
    status TEXT NOT NULL,
    created_at TEXT NOT NULL,
    expires_at TEXT NOT NULL,
    revoked_at TEXT
);
"""


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def now_iso() -> str:
    return now_utc().isoformat()


def hash_token(token: str, salt: str) -> str:
    return hashlib.sha256(f"{salt}:{token}".encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class Session:
    id: str
    actor: str
    token: str
    token_prefix: str
    scopes: tuple[str, ...]
    status: str = "active"
    created_at: str = field(default_factory=now_iso)
    expires_at: str = ""

    def to_public_dict(self) -> dict:
        return {
            "id": self.id,
            "actor": self.actor,
            "token_prefix": self.token_prefix,
            "scopes": list(self.scopes),
            "status": self.status,
            "created_at": self.created_at,
            "expires_at": self.expires_at,
        }


@dataclass(frozen=True)
class VerifiedSession:
    id: str
    actor: str
    scopes: tuple[str, ...]

    def to_dict(self) -> dict:
        return {"id": self.id, "actor": self.actor, "scopes": list(self.scopes)}


class SessionStore:
    def __init__(self, db_path: str | Path):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.db_path) as con:
            con.executescript(SCHEMA)

    def create_session(self, actor: str, scopes: tuple[str, ...] = ("operator",), ttl_hours: int = 12) -> Session:
        if not actor:
            raise ValueError("actor required")
        token = "zai_sess_" + secrets.token_urlsafe(32)
        prefix = token[:16]
        salt = secrets.token_hex(16)
        expires_at = (now_utc() + timedelta(hours=ttl_hours)).isoformat()
        session = Session(
            id=str(uuid.uuid4()),
            actor=actor,
            token=token,
            token_prefix=prefix,
            scopes=scopes,
            expires_at=expires_at,
        )
        with sqlite3.connect(self.db_path) as con:
            con.execute(
                """
                INSERT INTO sessions
                (id, actor, token_prefix, salt, token_hash, scopes_csv, status, created_at, expires_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (session.id, actor, prefix, salt, hash_token(token, salt), ",".join(scopes), session.status, session.created_at, session.expires_at),
            )
        return session

    def verify_session(self, token: str | None) -> VerifiedSession | None:
        if not token:
            return None
        prefix = token[:16]
        with sqlite3.connect(self.db_path) as con:
            row = con.execute(
                """
                SELECT id, actor, salt, token_hash, scopes_csv, status, expires_at
                FROM sessions
                WHERE token_prefix = ?
                """,
                (prefix,),
            ).fetchone()
        if not row:
            return None
        session_id, actor, salt, token_hash, scopes_csv, status, expires_at = row
        if status != "active":
            return None
        if now_utc() > datetime.fromisoformat(expires_at):
            return None
        if hash_token(token, salt) != token_hash:
            return None
        return VerifiedSession(id=session_id, actor=actor, scopes=tuple(s for s in scopes_csv.split(",") if s))

    def revoke_session(self, token: str) -> None:
        prefix = token[:16]
        with sqlite3.connect(self.db_path) as con:
            cur = con.execute(
                "UPDATE sessions SET status = 'revoked', revoked_at = ? WHERE token_prefix = ? AND status = 'active'",
                (now_iso(), prefix),
            )
            if cur.rowcount != 1:
                raise ValueError("active session not found")
