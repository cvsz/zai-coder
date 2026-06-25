from __future__ import annotations

import sqlite3
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass
class MemoryItem:
    key: str
    value: str
    namespace: str = "default"
    ts: float = 0.0


class MemoryStore:
    def __init__(self, path: str | Path):
        self.path = Path(path).expanduser()
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._init()

    def connect(self):
        return sqlite3.connect(str(self.path))

    def _init(self) -> None:
        with self.connect() as db:
            db.execute(
                """
                CREATE TABLE IF NOT EXISTS memory (
                  namespace TEXT NOT NULL,
                  key TEXT NOT NULL,
                  value TEXT NOT NULL,
                  ts REAL NOT NULL,
                  PRIMARY KEY(namespace, key)
                )
                """
            )
            db.execute(
                """
                CREATE TABLE IF NOT EXISTS runs (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  ts REAL NOT NULL,
                  agent TEXT NOT NULL,
                  task TEXT NOT NULL,
                  response TEXT NOT NULL,
                  model TEXT NOT NULL,
                  provider TEXT NOT NULL
                )
                """
            )

    def set(self, key: str, value: str, namespace: str = "default") -> None:
        with self.connect() as db:
            db.execute(
                "INSERT INTO memory(namespace,key,value,ts) VALUES(?,?,?,?) "
                "ON CONFLICT(namespace,key) DO UPDATE SET value=excluded.value, ts=excluded.ts",
                (namespace, key, value, time.time()),
            )

    def get(self, key: str, namespace: str = "default") -> str | None:
        with self.connect() as db:
            row = db.execute("SELECT value FROM memory WHERE namespace=? AND key=?", (namespace, key)).fetchone()
        return row[0] if row else None

    def list(self, namespace: str = "default", limit: int = 100) -> list[MemoryItem]:
        with self.connect() as db:
            rows = db.execute(
                "SELECT key,value,namespace,ts FROM memory WHERE namespace=? ORDER BY ts DESC LIMIT ?",
                (namespace, limit),
            ).fetchall()
        return [MemoryItem(*row) for row in rows]

    def delete(self, key: str, namespace: str = "default") -> bool:
        with self.connect() as db:
            cur = db.execute("DELETE FROM memory WHERE namespace=? AND key=?", (namespace, key))
            return cur.rowcount > 0

    def add_run(self, agent: str, task: str, response: str, model: str, provider: str) -> int:
        with self.connect() as db:
            cur = db.execute(
                "INSERT INTO runs(ts,agent,task,response,model,provider) VALUES(?,?,?,?,?,?)",
                (time.time(), agent, task, response, model, provider),
            )
            return int(cur.lastrowid)

    def recent_runs(self, limit: int = 20) -> list[dict[str, object]]:
        with self.connect() as db:
            rows = db.execute(
                "SELECT id,ts,agent,task,response,model,provider FROM runs ORDER BY id DESC LIMIT ?",
                (limit,),
            ).fetchall()
        keys = ["id", "ts", "agent", "task", "response", "model", "provider"]
        return [dict(zip(keys, row)) for row in rows]
