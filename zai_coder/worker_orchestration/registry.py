"""Worker registry."""

from __future__ import annotations

import json
import sqlite3
import uuid
from pathlib import Path

from .models import WorkerNode, now_iso


SCHEMA = """
CREATE TABLE IF NOT EXISTS worker_nodes (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    queue TEXT NOT NULL,
    tenant_scope TEXT NOT NULL,
    status TEXT NOT NULL,
    concurrency_limit INTEGER NOT NULL,
    heartbeat_at TEXT NOT NULL,
    created_at TEXT NOT NULL
);
"""


class WorkerRegistry:
    def __init__(self, db_path: str | Path = "data/worker-orchestration.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.db_path) as con:
            con.executescript(SCHEMA)

    def register(self, name: str, queue: str, tenant_scope: str = "shared", concurrency_limit: int = 1) -> WorkerNode:
        node = WorkerNode(
            id=f"worker_{uuid.uuid4().hex[:12]}",
            name=name,
            queue=queue,
            tenant_scope=tenant_scope,
            concurrency_limit=concurrency_limit,
        )
        issues = node.validate()
        if issues:
            raise ValueError("; ".join(issues))
        with sqlite3.connect(self.db_path) as con:
            con.execute(
                """
                INSERT INTO worker_nodes
                (id, name, queue, tenant_scope, status, concurrency_limit, heartbeat_at, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (node.id, node.name, node.queue, node.tenant_scope, node.status, node.concurrency_limit, node.heartbeat_at, node.created_at),
            )
        return node

    def heartbeat(self, worker_id: str, status: str = "idle") -> WorkerNode | None:
        heartbeat_at = now_iso()
        with sqlite3.connect(self.db_path) as con:
            con.execute("UPDATE worker_nodes SET heartbeat_at=?, status=? WHERE id=?", (heartbeat_at, status, worker_id))
            row = con.execute(
                "SELECT id, name, queue, tenant_scope, status, concurrency_limit, heartbeat_at, created_at FROM worker_nodes WHERE id=?",
                (worker_id,),
            ).fetchone()
        if not row:
            return None
        return WorkerNode(id=row[0], name=row[1], queue=row[2], tenant_scope=row[3], status=row[4], concurrency_limit=row[5], heartbeat_at=row[6], created_at=row[7])

    def list_workers(self, queue: str | None = None) -> list[dict]:
        with sqlite3.connect(self.db_path) as con:
            if queue:
                rows = con.execute(
                    "SELECT id, name, queue, tenant_scope, status, concurrency_limit, heartbeat_at, created_at FROM worker_nodes WHERE queue=? ORDER BY created_at DESC",
                    (queue,),
                ).fetchall()
            else:
                rows = con.execute(
                    "SELECT id, name, queue, tenant_scope, status, concurrency_limit, heartbeat_at, created_at FROM worker_nodes ORDER BY created_at DESC"
                ).fetchall()
        return [
            WorkerNode(id=r[0], name=r[1], queue=r[2], tenant_scope=r[3], status=r[4], concurrency_limit=r[5], heartbeat_at=r[6], created_at=r[7]).to_dict()
            for r in rows
        ]
