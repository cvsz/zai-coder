"""Checksum and release manifest helpers."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


def sha256_file(path: str | Path) -> str:
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def build_checksum_manifest(root: str | Path, patterns: tuple[str, ...] = ("*.zip", "*.tar.gz", "*.whl")) -> dict:
    root = Path(root)
    files = []
    for pattern in patterns:
        files.extend(root.glob(pattern))
    return {str(path.name): sha256_file(path) for path in sorted(files)}


def write_checksum_manifest(root: str | Path, out_file: str | Path = "SHA256SUMS.json") -> dict:
    manifest = build_checksum_manifest(root)
    Path(out_file).write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return manifest
