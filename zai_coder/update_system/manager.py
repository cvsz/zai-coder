"""Safe update system.

All mutation operations are dry-run by default. Set apply=True only after
reviewing the update plan and creating a checkpoint.
"""

from __future__ import annotations

import hashlib
import json
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List

from .manifest import UpdateManifest


BLOCKED_UPDATE_PATH_PARTS = {
    ".env",
    "node_modules",
    "dist",
    ".next",
    "coverage",
    "reports",
    "__pycache__",
    ".pytest_cache",
}


@dataclass
class UpdatePlan:
    version: str
    channel: str
    files: List[str]
    warnings: List[str]
    apply_required: bool = True

    def to_dict(self) -> dict:
        return {
            "version": self.version,
            "channel": self.channel,
            "files": list(self.files),
            "warnings": list(self.warnings),
            "apply_required": self.apply_required,
        }


class UpdateManager:
    def __init__(self, project_root: str | Path):
        self.project_root = Path(project_root)

    def checksum(self, path: str | Path) -> str:
        data = Path(path).read_bytes()
        return hashlib.sha256(data).hexdigest()

    def validate_paths(self, files: Iterable[str]) -> List[str]:
        warnings: List[str] = []
        for f in files:
            normalized = f.replace("\\", "/")
            if normalized.startswith("/") or ".." in normalized.split("/"):
                warnings.append(f"unsafe path: {f}")
            if normalized.startswith("apps/zlms/"):
                warnings.append(f"blocked apps/zlms path: {f}")
            if any(part in normalized.split("/") for part in BLOCKED_UPDATE_PATH_PARTS):
                warnings.append(f"blocked generated/secret path: {f}")
        return warnings

    def plan(self, manifest: UpdateManifest) -> UpdatePlan:
        warnings = self.validate_paths(manifest.files)
        return UpdatePlan(
            version=manifest.version,
            channel=manifest.channel,
            files=list(manifest.files),
            warnings=warnings,
            apply_required=True,
        )

    def apply_from_dir(self, source_dir: str | Path, manifest: UpdateManifest, apply: bool = False) -> UpdatePlan:
        plan = self.plan(manifest)
        if plan.warnings:
            return plan
        if not apply:
            return plan

        src_root = Path(source_dir)
        for rel in manifest.files:
            src = src_root / rel
            dst = self.project_root / rel
            if not src.exists():
                plan.warnings.append(f"missing source file: {rel}")
                continue
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
        return plan
