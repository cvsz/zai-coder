from __future__ import annotations

import os
import subprocess
from dataclasses import dataclass
from pathlib import Path

IGNORE_DIRS = {".git", "node_modules", "dist", "build", ".next", "coverage", ".venv", "venv", "__pycache__"}


@dataclass
class ProjectScan:
    root: str
    files: int
    dirs: int
    languages: dict[str, int]
    git_status: str
    notable_files: list[str]

    def to_markdown(self) -> str:
        lang = "\n".join(f"- {k}: {v}" for k, v in sorted(self.languages.items(), key=lambda x: (-x[1], x[0]))[:20])
        notable = "\n".join(f"- {p}" for p in self.notable_files[:40])
        return f"""# Project Scan\n\nRoot: `{self.root}`\n\nFiles: {self.files}\nDirs: {self.dirs}\n\n## Languages\n{lang or '- none'}\n\n## Notable files\n{notable or '- none'}\n\n## Git status\n```text\n{self.git_status.strip() or 'clean / not a git repo'}\n```\n"""


def scan_project(root: str | Path, max_files: int = 5000) -> ProjectScan:
    rootp = Path(root).expanduser().resolve()
    files = 0
    dirs = 0
    languages: dict[str, int] = {}
    notable: list[str] = []
    names = {"package.json", "pyproject.toml", "go.mod", "Cargo.toml", "Dockerfile", "docker-compose.yml", "README.md", "Makefile"}
    for current, dirnames, filenames in os.walk(rootp):
        dirnames[:] = [d for d in dirnames if d not in IGNORE_DIRS]
        dirs += len(dirnames)
        for name in filenames:
            files += 1
            rel = str((Path(current) / name).relative_to(rootp)).replace("\\", "/")
            ext = Path(name).suffix.lower() or "[no-ext]"
            languages[ext] = languages.get(ext, 0) + 1
            if name in names or rel.startswith(("apps/", "src/", "scripts/", ".github/workflows/")):
                notable.append(rel)
            if files >= max_files:
                break
        if files >= max_files:
            break
    try:
        proc = subprocess.run(["git", "status", "--short"], cwd=str(rootp), text=True, capture_output=True, timeout=20)
        status = proc.stdout or proc.stderr
    except Exception as exc:  # noqa: BLE001
        status = str(exc)
    return ProjectScan(str(rootp), files, dirs, languages, status, notable)
