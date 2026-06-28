from __future__ import annotations

import os
import shutil
from pathlib import Path
from typing import Any

from .safety import SafetyPolicy


class CheckpointManager:
    def __init__(self, workspace: str | Path, checkpoint_dir: str | Path = ".zai-coder/checkpoints"):
        self.workspace = Path(workspace).expanduser().resolve()
        self.checkpoint_dir = (self.workspace / checkpoint_dir).resolve() if not Path(checkpoint_dir).is_absolute() else Path(checkpoint_dir)
        self.safety = SafetyPolicy()

    def _get_checkpoint_path(self, checkpoint_id: str) -> Path:
        if "/" in checkpoint_id or "\\" in checkpoint_id or ".." in checkpoint_id:
            raise ValueError("Invalid checkpoint ID: path traversal blocked")
        return self.checkpoint_dir / checkpoint_id

    def list_checkpoints(self) -> list[dict[str, Any]]:
        if not self.checkpoint_dir.exists():
            return []
        
        checkpoints = []
        for entry in self.checkpoint_dir.iterdir():
            if entry.is_dir() and entry.name.startswith("patch-"):
                checkpoints.append(self.checkpoint_metadata(entry.name))
        
        # Sort by creation time descending (based on name which has stamp)
        checkpoints.sort(key=lambda x: x["id"], reverse=True)
        return checkpoints

    def checkpoint_metadata(self, checkpoint_id: str) -> dict[str, Any]:
        cp_path = self._get_checkpoint_path(checkpoint_id)
        if not cp_path.exists() or not cp_path.is_dir():
            raise FileNotFoundError(f"Checkpoint not found: {checkpoint_id}")
        
        files = []
        size_bytes = 0
        for root, _, filenames in os.walk(cp_path):
            for filename in filenames:
                filepath = Path(root) / filename
                rel_path = filepath.relative_to(cp_path)
                files.append(str(rel_path))
                size_bytes += filepath.stat().st_size
                
        return {
            "id": checkpoint_id,
            "path": str(cp_path),
            "files": sorted(files),
            "size_bytes": size_bytes,
        }

    def restore_checkpoint(self, checkpoint_id: str, dry_run: bool = True, allow_secrets: bool = False) -> dict[str, Any]:
        cp_path = self._get_checkpoint_path(checkpoint_id)
        if not cp_path.exists() or not cp_path.is_dir():
            raise FileNotFoundError(f"Checkpoint not found: {checkpoint_id}")
            
        metadata = self.checkpoint_metadata(checkpoint_id)
        files_to_restore = metadata["files"]
        
        # Validate paths
        for rel_path in files_to_restore:
            if ".." in rel_path or rel_path.startswith("/"):
                raise ValueError(f"Path traversal detected in checkpoint file: {rel_path}")
            
            # Check safety
            safety_check = self.safety.check_path(rel_path)
            if not safety_check.allowed:
                raise ValueError(f"Safety violation: {safety_check.reason}")
            
            if not allow_secrets and "secret" in str(rel_path).lower():
                # Primitive secret check based on path name for safety
                raise ValueError(f"Cannot restore over secret file without explicit flag: {rel_path}")

            target_path = (self.workspace / rel_path).resolve()
            if not str(target_path).startswith(str(self.workspace)):
                raise ValueError(f"Path escapes workspace: {target_path}")

        if dry_run:
            return {
                "restored": False,
                "dry_run": True,
                "files": files_to_restore
            }
            
        for rel_path in files_to_restore:
            src_path = cp_path / rel_path
            target_path = (self.workspace / rel_path).resolve()
            
            target_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src_path, target_path)
            
        return {
            "restored": True,
            "dry_run": False,
            "files": files_to_restore
        }

    def delete_checkpoint(self, checkpoint_id: str, dry_run: bool = True) -> bool:
        cp_path = self._get_checkpoint_path(checkpoint_id)
        if not cp_path.exists() or not cp_path.is_dir():
            raise FileNotFoundError(f"Checkpoint not found: {checkpoint_id}")
            
        if dry_run:
            return False
            
        shutil.rmtree(cp_path)
        return True
