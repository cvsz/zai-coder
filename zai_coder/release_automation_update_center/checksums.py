"""Checksum and artifact verification."""

from __future__ import annotations

import hashlib
from pathlib import Path


def sha256_file(path: str | Path) -> str:
    p = Path(path)
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def artifact_manifest(path: str | Path) -> dict:
    p = Path(path)
    if not p.exists():
        return {"ok": False, "path": str(p), "reason": "artifact missing"}
    return {"ok": True, "path": str(p), "size_bytes": p.stat().st_size, "sha256": sha256_file(p)}


def verify_artifact(path: str | Path, expected_sha256: str) -> dict:
    manifest = artifact_manifest(path)
    if not manifest["ok"]:
        return manifest
    return {
        **manifest,
        "expected_sha256": expected_sha256,
        "matches": manifest["sha256"] == expected_sha256,
    }
