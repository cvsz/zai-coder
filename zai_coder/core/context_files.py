from pathlib import Path
from zai_coder.core.safety import SafetyPolicy

SUPPORTED_CONTEXT_FILES = [
    ".zai.md",
    ".hermes.md",
    "AGENTS.md",
    "CLAUDE.md",
    "SOUL.md",
    ".cursorrules"
]

class ContextFileDiscoverer:
    def __init__(self, workspace: Path, safety_policy: SafetyPolicy):
        self.workspace = workspace
        self.safety_policy = safety_policy
        self.max_size_bytes = 100 * 1024 # 100KB limit
        
    def discover(self) -> list[Path]:
        found = []
        # Check workspace root for supported files
        for name in SUPPORTED_CONTEXT_FILES:
            path = self.workspace / name
            if path.exists() and path.is_file():
                if self.safety_policy.check_path(str(path)).allowed:
                    if path.stat().st_size <= self.max_size_bytes:
                        found.append(path)
        return found
        
    def load(self, path: Path) -> str:
        if path not in self.discover():
            return ""
        return path.read_text(errors="replace")
