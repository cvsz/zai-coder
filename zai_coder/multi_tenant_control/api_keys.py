"""Tenant-scoped API keys."""

from __future__ import annotations

import hashlib
import secrets
import sqlite3
import uuid
from pathlib import Path

from .models import TenantScopedApiKey


SCHEMA = """
CREATE TABLE IF NOT EXISTS tenant_api_keys (
    id TEXT PRIMARY KEY,
    org_id TEXT NOT NULL,
    workspace_id TEXT NOT NULL,
    name TEXT NOT NULL,
    token_prefix TEXT NOT NULL,
    salt TEXT NOT NULL,
    token_hash TEXT NOT NULL,
    scopes_csv TEXT NOT NULL,
    status TEXT NOT NULL,
    created_at TEXT NOT NULL
);
"""


def hash_token(token: str, salt: str) -> str:
    return hashlib.sha256(f"{salt}:{token}".encode("utf-8")).hexdigest()


class TenantApiKeyStore:
    def __init__(self, db_path: str | Path = "data/tenant-api-keys.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.db_path) as con:
            con.executescript(SCHEMA)

    def create_key(self, org_id: str, workspace_id: str, name: str, scopes: tuple[str, ...] = ("workspace:view",)) -> tuple[TenantScopedApiKey, str]:
        token = "zai_tenant_" + secrets.token_urlsafe(32)
        salt = secrets.token_hex(16)
        key = TenantScopedApiKey(
            id=f"tak_{uuid.uuid4().hex[:12]}",
            org_id=org_id,
            workspace_id=workspace_id,
            name=name,
            token_prefix=token[:18],
            scopes=scopes,
        )
        with sqlite3.connect(self.db_path) as con:
            con.execute(
                """
                INSERT INTO tenant_api_keys
                (id, org_id, workspace_id, name, token_prefix, salt, token_hash, scopes_csv, status, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (key.id, key.org_id, key.workspace_id, key.name, key.token_prefix, salt, hash_token(token, salt), ",".join(scopes), key.status, key.created_at),
            )
        return key, token

    def verify_key(self, token: str | None, org_id: str, workspace_id: str, scope: str = "workspace:view") -> dict:
        if not token:
            return {"allowed": False, "reason": "missing token"}
        prefix = token[:18]
        with sqlite3.connect(self.db_path) as con:
            row = con.execute(
                """
                SELECT org_id, workspace_id, salt, token_hash, scopes_csv, status
                FROM tenant_api_keys WHERE token_prefix=?
                """,
                (prefix,),
            ).fetchone()
        if not row:
            return {"allowed": False, "reason": "key not found"}
        row_org, row_ws, salt, token_hash, scopes_csv, status = row
        if status != "active":
            return {"allowed": False, "reason": "key inactive"}
        if row_org != org_id or row_ws != workspace_id:
            return {"allowed": False, "reason": "tenant scope mismatch"}
        if hash_token(token, salt) != token_hash:
            return {"allowed": False, "reason": "invalid token"}
        scopes = tuple(s for s in scopes_csv.split(",") if s)
        if scope not in scopes and "workspace:*" not in scopes and "tenant:*" not in scopes:
            return {"allowed": False, "reason": f"missing scope: {scope}"}
        return {"allowed": True, "reason": "allowed", "scopes": list(scopes)}
