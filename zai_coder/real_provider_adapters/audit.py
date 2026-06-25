from __future__ import annotations
import json, sqlite3, uuid
from dataclasses import dataclass, field
from pathlib import Path
from .models import now_iso, ProviderContext, ProviderOperation, ProviderResult

SCHEMA = """
CREATE TABLE IF NOT EXISTS provider_audit_events (
    id TEXT PRIMARY KEY,
    provider TEXT NOT NULL,
    action TEXT NOT NULL,
    target TEXT NOT NULL,
    actor TEXT NOT NULL,
    dry_run INTEGER NOT NULL,
    ok INTEGER NOT NULL,
    operation_json TEXT NOT NULL,
    context_json TEXT NOT NULL,
    result_json TEXT NOT NULL,
    created_at TEXT NOT NULL
);
"""

@dataclass(frozen=True)
class ProviderAuditEvent:
    id: str
    provider: str
    action: str
    target: str
    actor: str
    dry_run: bool
    ok: bool
    created_at: str = field(default_factory=now_iso)
    def to_dict(self) -> dict:
        return self.__dict__.copy()

class ProviderAuditLog:
    def __init__(self, db_path: str | Path = 'data/provider-audit.db'):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.db_path) as con:
            con.executescript(SCHEMA)
    def record(self, context: ProviderContext, operation: ProviderOperation, result: ProviderResult) -> ProviderAuditEvent:
        event = ProviderAuditEvent(id=str(uuid.uuid4()), provider=operation.provider, action=operation.action, target=operation.target, actor=context.actor, dry_run=result.dry_run, ok=result.ok)
        with sqlite3.connect(self.db_path) as con:
            con.execute(
                """INSERT INTO provider_audit_events
                (id, provider, action, target, actor, dry_run, ok, operation_json, context_json, result_json, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (event.id, event.provider, event.action, event.target, event.actor, int(event.dry_run), int(event.ok), json.dumps(operation.to_dict(), sort_keys=True), json.dumps(context.to_safe_dict(), sort_keys=True), json.dumps(result.to_dict(), sort_keys=True), event.created_at),
            )
        return event
    def list_events(self, limit: int = 50) -> list[dict]:
        with sqlite3.connect(self.db_path) as con:
            rows = con.execute(
                """SELECT id, provider, action, target, actor, dry_run, ok, created_at
                FROM provider_audit_events ORDER BY created_at DESC LIMIT ?""",
                (limit,),
            ).fetchall()
        return [{'id': r[0], 'provider': r[1], 'action': r[2], 'target': r[3], 'actor': r[4], 'dry_run': bool(r[5]), 'ok': bool(r[6]), 'created_at': r[7]} for r in rows]
