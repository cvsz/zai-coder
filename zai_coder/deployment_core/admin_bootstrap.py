"""Admin bootstrap helper."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from zai_coder.app_studio.api_auth import ApiKeyManager


@dataclass(frozen=True)
class BootstrapResult:
    dry_run: bool
    admin_email: str
    api_key_id: str = ""
    raw_api_key: str = ""

    def to_dict(self) -> dict:
        return {
            "dry_run": self.dry_run,
            "admin_email": self.admin_email,
            "api_key_id": self.api_key_id,
            "raw_api_key": self.raw_api_key,
        }


def bootstrap_admin(db_path: str | Path, admin_email: str, apply: bool = False) -> BootstrapResult:
    if not admin_email or "@" not in admin_email:
        raise ValueError("admin_email must be an email address")
    if not apply:
        return BootstrapResult(dry_run=True, admin_email=admin_email)

    manager = ApiKeyManager(db_path)
    record, raw_key = manager.create_key(f"admin:{admin_email}")
    return BootstrapResult(dry_run=False, admin_email=admin_email, api_key_id=record.id, raw_api_key=raw_key)
