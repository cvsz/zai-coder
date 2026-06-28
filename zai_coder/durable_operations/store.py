"""Durable operations module for v52."""

import sqlite3
import json
from pathlib import Path
from typing import Any, Dict, List, Optional
import datetime

class DurableStore:
    def __init__(self, db_path: str = ":memory:"):
        self.db_path = db_path
        self._init_db()

    def _get_conn(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        with self._get_conn() as conn:
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS kpi_snapshots (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    data JSON NOT NULL
                );
                CREATE TABLE IF NOT EXISTS health_trends (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    status TEXT NOT NULL,
                    data JSON NOT NULL
                );
                CREATE TABLE IF NOT EXISTS compliance_evidence (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    evidence_type TEXT NOT NULL,
                    data JSON NOT NULL
                );
                CREATE TABLE IF NOT EXISTS audit_streams (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    event_type TEXT NOT NULL,
                    data JSON NOT NULL
                );
                CREATE TABLE IF NOT EXISTS release_evidence (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    version TEXT NOT NULL,
                    data JSON NOT NULL
                );
            """)

    def _insert(self, table: str, **kwargs):
        columns = ", ".join(kwargs.keys())
        placeholders = ", ".join("?" for _ in kwargs)
        values = tuple(kwargs.values())
        with self._get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute(f"INSERT INTO {table} ({columns}) VALUES ({placeholders})", values)
            return cursor.lastrowid

    def add_kpi_snapshot(self, data: Dict[str, Any]) -> int:
        return self._insert(
            "kpi_snapshots",
            timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            data=json.dumps(data)
        )

    def add_health_trend(self, status: str, data: Dict[str, Any]) -> int:
        return self._insert(
            "health_trends",
            timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            status=status,
            data=json.dumps(data)
        )

    def add_compliance_evidence(self, evidence_type: str, data: Dict[str, Any]) -> int:
        return self._insert(
            "compliance_evidence",
            timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            evidence_type=evidence_type,
            data=json.dumps(data)
        )

    def add_audit_stream(self, event_type: str, data: Dict[str, Any]) -> int:
        return self._insert(
            "audit_streams",
            timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            event_type=event_type,
            data=json.dumps(data)
        )

    def add_release_evidence(self, version: str, data: Dict[str, Any]) -> int:
        return self._insert(
            "release_evidence",
            timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            version=version,
            data=json.dumps(data)
        )

    def apply_retention_policy(self, table: str, days: int):
        cutoff = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=days)).isoformat()
        with self._get_conn() as conn:
            conn.execute(f"DELETE FROM {table} WHERE timestamp < ?", (cutoff,))

    def get_all(self, table: str, limit: int = 100) -> List[Dict[str, Any]]:
        with self._get_conn() as conn:
            rows = conn.execute(f"SELECT * FROM {table} ORDER BY timestamp DESC LIMIT ?", (limit,)).fetchall()
            return [dict(row) for row in rows]
