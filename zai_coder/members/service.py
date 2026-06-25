"""SQLite-backed member service.

This module is intentionally dependency-free and safe by default.
It stores local team state only; no emails are sent automatically.
"""

from __future__ import annotations

import json
import sqlite3
import uuid
from pathlib import Path
from typing import Iterable, List, Optional

from .models import Invite, Member, now_iso
from .roles import normalize_role, has_permission


SCHEMA = """
CREATE TABLE IF NOT EXISTS members (
    id TEXT PRIMARY KEY,
    email TEXT NOT NULL UNIQUE,
    display_name TEXT NOT NULL,
    roles_json TEXT NOT NULL,
    status TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS member_invites (
    id TEXT PRIMARY KEY,
    email TEXT NOT NULL,
    roles_json TEXT NOT NULL,
    invited_by TEXT NOT NULL,
    status TEXT NOT NULL,
    created_at TEXT NOT NULL
);
"""


class MemberService:
    def __init__(self, db_path: str | Path):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init()

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def _init(self) -> None:
        with self._connect() as con:
            con.executescript(SCHEMA)

    def add_member(self, email: str, display_name: str, roles: Iterable[str]) -> Member:
        roles_list = [normalize_role(r) for r in roles]
        member = Member(
            id=str(uuid.uuid4()),
            email=email.strip().lower(),
            display_name=display_name.strip(),
            roles=roles_list,
        )
        with self._connect() as con:
            con.execute(
                """
                INSERT INTO members
                (id, email, display_name, roles_json, status, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    member.id,
                    member.email,
                    member.display_name,
                    json.dumps(member.roles),
                    member.status,
                    member.created_at,
                    member.updated_at,
                ),
            )
        return member

    def list_members(self) -> List[Member]:
        with self._connect() as con:
            rows = con.execute(
                "SELECT id, email, display_name, roles_json, status, created_at, updated_at FROM members ORDER BY created_at"
            ).fetchall()
        return [
            Member(
                id=row[0],
                email=row[1],
                display_name=row[2],
                roles=json.loads(row[3]),
                status=row[4],
                created_at=row[5],
                updated_at=row[6],
            )
            for row in rows
        ]

    def get_member(self, email: str) -> Optional[Member]:
        with self._connect() as con:
            row = con.execute(
                "SELECT id, email, display_name, roles_json, status, created_at, updated_at FROM members WHERE email = ?",
                (email.strip().lower(),),
            ).fetchone()
        if not row:
            return None
        return Member(
            id=row[0],
            email=row[1],
            display_name=row[2],
            roles=json.loads(row[3]),
            status=row[4],
            created_at=row[5],
            updated_at=row[6],
        )

    def update_roles(self, email: str, roles: Iterable[str]) -> Member:
        roles_list = [normalize_role(r) for r in roles]
        updated_at = now_iso()
        with self._connect() as con:
            cur = con.execute(
                "UPDATE members SET roles_json = ?, updated_at = ? WHERE email = ?",
                (json.dumps(roles_list), updated_at, email.strip().lower()),
            )
            if cur.rowcount != 1:
                raise KeyError(f"member not found: {email}")
        member = self.get_member(email)
        assert member is not None
        return member

    def can(self, email: str, permission: str) -> bool:
        member = self.get_member(email)
        if not member or member.status != "active":
            return False
        return has_permission(member.roles, permission)

    def create_invite(self, email: str, roles: Iterable[str], invited_by: str) -> Invite:
        invite = Invite(
            id=str(uuid.uuid4()),
            email=email.strip().lower(),
            roles=[normalize_role(r) for r in roles],
            invited_by=invited_by,
        )
        with self._connect() as con:
            con.execute(
                """
                INSERT INTO member_invites
                (id, email, roles_json, invited_by, status, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    invite.id,
                    invite.email,
                    json.dumps(invite.roles),
                    invite.invited_by,
                    invite.status,
                    invite.created_at,
                ),
            )
        return invite
