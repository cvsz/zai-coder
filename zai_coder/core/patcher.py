from __future__ import annotations

import hashlib
import shutil
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path

from .safety import SafetyPolicy


@dataclass
class PatchResult:
    ok: bool
    stdout: str = ""
    stderr: str = ""
    blocked_reason: str = ""
    checkpoint: str = ""


class PatchRuntime:
    def __init__(self, workspace: str | Path, checkpoint_dir: str | Path, safety: SafetyPolicy | None = None):
        self.workspace = Path(workspace).expanduser().resolve()
        self.checkpoint_dir = (self.workspace / checkpoint_dir).resolve() if not Path(checkpoint_dir).is_absolute() else Path(checkpoint_dir)
        self.safety = safety or SafetyPolicy()

    def _extract_paths(self, patch_text: str) -> list[str]:
        paths: list[str] = []
        for line in patch_text.splitlines():
            if line.startswith("+++ b/") or line.startswith("--- a/"):
                p = line[6:].strip()
                if p != "/dev/null":
                    paths.append(p)
        return sorted(set(paths))

    def _checkpoint(self, paths: list[str]) -> str:
        stamp = time.strftime("%Y%m%d-%H%M%S")
        digest = hashlib.sha1((stamp + "\n" + "\n".join(paths)).encode()).hexdigest()[:8]
        dest = self.checkpoint_dir / f"patch-{stamp}-{digest}"
        dest.mkdir(parents=True, exist_ok=True)
        for rel in paths:
            src = (self.workspace / rel).resolve()
            if src.exists() and src.is_file() and str(src).startswith(str(self.workspace)):
                out = dest / rel
                out.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, out)
        return str(dest)

    def apply(self, patch_text: str, check_only: bool = False) -> PatchResult:
        paths = self._extract_paths(patch_text)
        if not paths:
            return PatchResult(False, blocked_reason="No file paths found in unified diff")
        for rel in paths:
            path_check = self.safety.check_path(rel)
            if not path_check.allowed:
                return PatchResult(False, blocked_reason=path_check.reason)
        checkpoint = self._checkpoint(paths) if not check_only else ""
        args = ["git", "apply", "--check"] if check_only else ["git", "apply"]
        proc = subprocess.run(args, cwd=str(self.workspace), input=patch_text, text=True, capture_output=True, timeout=120)
        return PatchResult(
            ok=proc.returncode == 0,
            stdout=proc.stdout,
            stderr=proc.stderr,
            checkpoint=checkpoint,
        )

    def apply_file(self, patch_file: str | Path, check_only: bool = False) -> PatchResult:
        patch_path = Path(patch_file).expanduser()
        text = patch_path.read_text(encoding="utf-8", errors="replace")
        return self.apply(text, check_only=check_only)
