"""PostgreSQL adapter.

Uses psycopg when installed. Tests can exercise DSN validation without opening a
network connection.
"""

from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import urlparse


@dataclass(frozen=True)
class PostgresSettings:
    dsn: str
    connect_timeout_seconds: int = 5
    application_name: str = "zai-coder"

    def validate(self) -> list[str]:
        issues = []
        parsed = urlparse(self.dsn)
        if parsed.scheme not in {"postgresql", "postgres"}:
            issues.append("dsn must start with postgresql:// or postgres://")
        if not parsed.hostname:
            issues.append("dsn host required")
        if not parsed.path or parsed.path == "/":
            issues.append("database name required")
        return issues

    def safe_dict(self) -> dict:
        parsed = urlparse(self.dsn)
        return {
            "scheme": parsed.scheme,
            "host": parsed.hostname,
            "port": parsed.port or 5432,
            "database": parsed.path.lstrip("/"),
            "connect_timeout_seconds": self.connect_timeout_seconds,
            "application_name": self.application_name,
        }


class PostgresAdapter:
    def __init__(self, settings: PostgresSettings):
        issues = settings.validate()
        if issues:
            raise ValueError("; ".join(issues))
        self.settings = settings

    def connection_kwargs(self) -> dict:
        safe = self.settings.safe_dict()
        return {
            "connect_timeout": self.settings.connect_timeout_seconds,
            "application_name": self.settings.application_name,
            "target_session_attrs": "read-write",
            "safe": safe,
        }

    def connect(self):
        try:
            import psycopg
        except ImportError as exc:
            raise RuntimeError("psycopg is not installed. Install requirements-production.txt.") from exc
        return psycopg.connect(self.settings.dsn, connect_timeout=self.settings.connect_timeout_seconds, application_name=self.settings.application_name)
