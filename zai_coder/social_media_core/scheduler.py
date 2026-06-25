"""Dry-run-first social scheduler.

This scheduler stores intent locally. It does not post to external platforms.
External posting adapters must require explicit credentials and APPLY=1.
"""

from __future__ import annotations

import json
import sqlite3
import uuid
from pathlib import Path
from typing import List

from .composer import SocialPost, validate_post


SCHEMA = """
CREATE TABLE IF NOT EXISTS social_posts (
    id TEXT PRIMARY KEY,
    platform TEXT NOT NULL,
    text TEXT NOT NULL,
    campaign TEXT NOT NULL,
    media_json TEXT NOT NULL,
    status TEXT NOT NULL,
    scheduled_at TEXT
);
"""


class SocialScheduler:
    def __init__(self, db_path: str | Path):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.db_path) as con:
            con.executescript(SCHEMA)

    def schedule(self, post: SocialPost, scheduled_at: str, apply: bool = False) -> dict:
        issues = validate_post(post)
        result = {
            "id": str(uuid.uuid4()),
            "dry_run": not apply,
            "scheduled_at": scheduled_at,
            "issues": issues,
            "post": post.to_dict(),
        }
        if issues or not apply:
            return result
        with sqlite3.connect(self.db_path) as con:
            con.execute(
                """
                INSERT INTO social_posts
                (id, platform, text, campaign, media_json, status, scheduled_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    result["id"],
                    post.platform,
                    post.text,
                    post.campaign,
                    json.dumps(post.media_paths),
                    "scheduled",
                    scheduled_at,
                ),
            )
        result["post"]["status"] = "scheduled"
        return result

    def list_posts(self) -> List[dict]:
        with sqlite3.connect(self.db_path) as con:
            rows = con.execute(
                "SELECT id, platform, text, campaign, media_json, status, scheduled_at FROM social_posts ORDER BY scheduled_at"
            ).fetchall()
        return [
            {
                "id": row[0],
                "platform": row[1],
                "text": row[2],
                "campaign": row[3],
                "media_paths": json.loads(row[4]),
                "status": row[5],
                "scheduled_at": row[6],
            }
            for row in rows
        ]
