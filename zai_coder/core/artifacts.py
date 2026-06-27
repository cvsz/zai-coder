from __future__ import annotations

import hashlib
import json
import sqlite3
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .safety import SafetyPolicy


ARTIFACT_SCHEMA_VERSION = 1
ARTIFACT_KINDS = {
    "code",
    "doc",
    "image",
    "audio",
    "video",
    "archive",
    "report",
    "test-output",
    "other",
}


@dataclass(frozen=True)
class ArtifactRecord:
    id: int
    path: str
    label: str
    kind: str
    sha256: str
    size_bytes: int
    description: str
    tags: tuple[str, ...]
    created_at: float

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "path": self.path,
            "label": self.label,
            "kind": self.kind,
            "sha256": self.sha256,
            "size_bytes": self.size_bytes,
            "description": self.description,
            "tags": list(self.tags),
            "created_at": self.created_at,
        }


def sha256_file(path: str | Path) -> str:
    h = hashlib.sha256()
    with Path(path).open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


class ArtifactStore:
    def __init__(self, workspace: str | Path = ".", db_path: str | Path | None = None):
        self.workspace = Path(workspace).expanduser().resolve()
        self.db_path = Path(db_path).expanduser().resolve() if db_path else self.workspace / ".zai-coder" / "artifacts" / "artifacts.db"
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(self.db_path))
        self.conn.row_factory = sqlite3.Row
        self._init_db()

    def _init_db(self) -> None:
        with self.conn:
            self.conn.execute(
                """
                CREATE TABLE IF NOT EXISTS artifact_schema_version (
                    name TEXT PRIMARY KEY,
                    version INTEGER NOT NULL,
                    updated_at REAL NOT NULL
                )
                """
            )
            self.conn.execute(
                """
                CREATE TABLE IF NOT EXISTS artifacts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    path TEXT NOT NULL,
                    label TEXT NOT NULL,
                    kind TEXT NOT NULL,
                    sha256 TEXT NOT NULL,
                    size_bytes INTEGER NOT NULL,
                    description TEXT NOT NULL,
                    tags_json TEXT NOT NULL,
                    created_at REAL NOT NULL
                )
                """
            )
            self.conn.execute(
                """
                INSERT INTO artifact_schema_version (name, version, updated_at)
                VALUES ('artifacts', ?, ?)
                ON CONFLICT(name) DO UPDATE SET version=excluded.version, updated_at=excluded.updated_at
                """,
                (ARTIFACT_SCHEMA_VERSION, time.time()),
            )

    def _resolve_artifact_path(self, path: str | Path) -> Path:
        candidate = Path(path).expanduser()
        if not candidate.is_absolute():
            candidate = self.workspace / candidate
        candidate = candidate.resolve()
        if not str(candidate).startswith(str(self.workspace)):
            raise ValueError("Artifact path must stay inside workspace")
        rel = candidate.relative_to(self.workspace).as_posix()
        decision = SafetyPolicy().check_path(rel)
        if not decision.allowed:
            raise ValueError(decision.reason)
        if not candidate.exists() or not candidate.is_file():
            raise FileNotFoundError(f"Artifact file not found: {rel}")
        return candidate

    def _row_to_record(self, row: sqlite3.Row) -> ArtifactRecord:
        return ArtifactRecord(
            id=int(row["id"]),
            path=row["path"],
            label=row["label"],
            kind=row["kind"],
            sha256=row["sha256"],
            size_bytes=int(row["size_bytes"]),
            description=row["description"],
            tags=tuple(json.loads(row["tags_json"] or "[]")),
            created_at=float(row["created_at"]),
        )

    def add(
        self,
        path: str | Path,
        *,
        label: str = "",
        kind: str = "other",
        description: str = "",
        tags: tuple[str, ...] = (),
    ) -> dict[str, Any]:
        normalized_kind = str(kind or "other").strip().lower()
        if normalized_kind not in ARTIFACT_KINDS:
            raise ValueError(f"Unsupported artifact kind: {kind}")
        artifact_path = self._resolve_artifact_path(path)
        rel = artifact_path.relative_to(self.workspace).as_posix()
        now = time.time()
        with self.conn:
            cur = self.conn.execute(
                """
                INSERT INTO artifacts (path, label, kind, sha256, size_bytes, description, tags_json, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    rel,
                    label or artifact_path.name,
                    normalized_kind,
                    sha256_file(artifact_path),
                    artifact_path.stat().st_size,
                    description,
                    json.dumps(list(tags), sort_keys=True),
                    now,
                ),
            )
        record = self.get(int(cur.lastrowid))
        if record is None:
            raise RuntimeError("created artifact could not be loaded")
        return record

    def list(self, kind: str | None = None) -> list[dict[str, Any]]:
        if kind:
            normalized_kind = str(kind).strip().lower()
            cur = self.conn.execute("SELECT * FROM artifacts WHERE kind = ? ORDER BY created_at DESC, id DESC", (normalized_kind,))
        else:
            cur = self.conn.execute("SELECT * FROM artifacts ORDER BY created_at DESC, id DESC")
        return [self._row_to_record(row).to_dict() for row in cur.fetchall()]

    def get(self, artifact_id: int) -> dict[str, Any] | None:
        cur = self.conn.execute("SELECT * FROM artifacts WHERE id = ?", (artifact_id,))
        row = cur.fetchone()
        return self._row_to_record(row).to_dict() if row else None

    def export_json(self) -> dict[str, Any]:
        return {
            "schema_version": {"name": "artifacts", "version": ARTIFACT_SCHEMA_VERSION},
            "artifacts": self.list(),
        }

