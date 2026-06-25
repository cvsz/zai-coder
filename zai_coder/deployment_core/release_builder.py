"""Release artifact builder."""

from __future__ import annotations

import shutil
import time
import zipfile
from dataclasses import dataclass
from pathlib import Path


EXCLUDE_PARTS = {".git", "__pycache__", ".pytest_cache", "node_modules", "dist", ".next", "coverage", "reports"}


@dataclass(frozen=True)
class ReleaseArtifact:
    path: str
    dry_run: bool
    file_count: int

    def to_dict(self) -> dict:
        return {"path": self.path, "dry_run": self.dry_run, "file_count": self.file_count}


def should_include(rel: Path) -> bool:
    if any(part in EXCLUDE_PARTS for part in rel.parts):
        return False
    normalized = str(rel).replace("\\", "/")
    if normalized.startswith("apps/zlms/"):
        return False
    if rel.name.startswith(".env"):
        return False
    return True


def build_release_zip(project_root: str | Path, output_dir: str | Path = "release", name: str = "zai-coder-release", apply: bool = False) -> ReleaseArtifact:
    root = Path(project_root)
    out = Path(output_dir)
    target = out / f"{name}-{time.strftime('%Y%m%d-%H%M%S')}.zip"
    files = [p for p in root.rglob("*") if p.is_file() and should_include(p.relative_to(root))]
    if not apply:
        return ReleaseArtifact(str(target), True, len(files))

    out.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(target, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for p in files:
            z.write(p, p.relative_to(root))
    return ReleaseArtifact(str(target), False, len(files))
