"""Backup and restore helpers.

Backups are tar.gz archives. Restore is dry-run by default and requires apply=True.
"""

from __future__ import annotations

import tarfile
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


BLOCKED_PARTS = {".git", "node_modules", "dist", ".next", "coverage", "reports", "__pycache__", ".pytest_cache"}


@dataclass(frozen=True)
class BackupPlan:
    archive_path: str
    files: list[str]
    dry_run: bool = True

    def to_dict(self) -> dict:
        return {"archive_path": self.archive_path, "files": list(self.files), "dry_run": self.dry_run}


def is_backup_allowed(path: Path) -> bool:
    parts = set(path.parts)
    if parts & BLOCKED_PARTS:
        return False
    normalized = str(path).replace("\\", "/")
    if normalized.startswith("apps/zlms/") or "/apps/zlms/" in normalized:
        return False
    return path.is_file()


def create_backup(project_root: str | Path, output_dir: str | Path = "backups", apply: bool = False) -> BackupPlan:
    root = Path(project_root)
    out = Path(output_dir)
    archive = out / f"zai-backup-{time.strftime('%Y%m%d-%H%M%S')}.tar.gz"
    files = [p for p in root.rglob("*") if is_backup_allowed(p.relative_to(root))]
    rels = [str(p.relative_to(root)) for p in files]

    if not apply:
        return BackupPlan(str(archive), rels, dry_run=True)

    out.mkdir(parents=True, exist_ok=True)
    with tarfile.open(archive, "w:gz") as tar:
        for p in files:
            tar.add(p, arcname=str(p.relative_to(root)))
    return BackupPlan(str(archive), rels, dry_run=False)


def _unsafe_archive_entries(members: Iterable[tarfile.TarInfo]) -> list[str]:
    unsafe = []
    for member in members:
        normalized = member.name.replace("\\", "/")
        parts = Path(normalized).parts
        if normalized.startswith("/") or ".." in parts or normalized.startswith("apps/zlms/"):
            unsafe.append(member.name)
            continue
        if not (member.isfile() or member.isdir()):
            unsafe.append(member.name)
    return unsafe


def restore_backup(archive_path: str | Path, project_root: str | Path, apply: bool = False) -> dict:
    archive = Path(archive_path)
    root = Path(project_root)
    if not archive.exists():
        raise FileNotFoundError(str(archive))
    with tarfile.open(archive, "r:gz") as tar:
        members = tar.getmembers()
        names = [member.name for member in members]
        unsafe = _unsafe_archive_entries(members)
        if unsafe:
            raise ValueError(f"unsafe archive entries: {unsafe[:5]}")
        if not apply:
            return {"dry_run": True, "archive": str(archive), "files": names}
        tar.extractall(root)
        return {"dry_run": False, "archive": str(archive), "files": names}
