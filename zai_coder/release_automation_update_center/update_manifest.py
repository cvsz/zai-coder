"""Update manifest builder."""

from __future__ import annotations

import json
import uuid
from pathlib import Path

from .models import UpdateManifest
from .checksums import artifact_manifest


def build_update_manifest(version: str, channel: str, package_name: str, artifact_path: str) -> UpdateManifest:
    artifact = artifact_manifest(artifact_path)
    manifest = UpdateManifest(
        id=f"upd_{uuid.uuid4().hex[:12]}",
        version=version,
        channel=channel,
        package_name=package_name,
        artifact_path=artifact_path,
        sha256=artifact.get("sha256", ""),
        size_bytes=int(artifact.get("size_bytes", 0) or 0),
    )
    issues = manifest.validate()
    if issues:
        raise ValueError("; ".join(issues))
    return manifest


def write_update_manifest(manifest: UpdateManifest, root: str | Path = ".", out_dir: str = "updates/manifests") -> str:
    root = Path(root)
    path = root / out_dir / f"{manifest.version}-{manifest.channel}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(manifest.to_dict(), indent=2, sort_keys=True), encoding="utf-8")
    return str(path)


def update_manifest_schema() -> dict:
    return {
        "required": ["id", "version", "channel", "package_name", "artifact_path", "sha256", "rollback_supported"],
        "channels": ["dev", "alpha", "beta", "rc", "stable", "lts"],
        "safe_defaults": {"dry_run_update": True, "rollback_supported": True, "approval_required": True},
    }
