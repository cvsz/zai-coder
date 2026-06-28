import re
import subprocess
from pathlib import Path
from zai_coder.core.safety import SafetyPolicy

class ContextReferenceParser:
    def __init__(self, workspace: Path, safety_policy: SafetyPolicy):
        self.workspace = workspace
        self.safety_policy = safety_policy
        self.ref_pattern = re.compile(r"@(?:file|dir|git):[a-zA-Z0-9_\-\./\\]+")
        
    def resolve_references(self, text: str) -> dict[str, str]:
        resolved = {}
        for match in self.ref_pattern.findall(text):
            if match.startswith("@file:"):
                path_str = match[6:]
                p = (self.workspace / path_str).resolve()
                if p.is_relative_to(self.workspace) and p.is_file():
                    if self.safety_policy.check_path(str(p)).allowed:
                        try:
                            resolved[match] = p.read_text(errors="replace")
                        except Exception as e:
                            resolved[match] = f"Error reading file: {e}"
            elif match.startswith("@dir:"):
                path_str = match[5:]
                p = (self.workspace / path_str).resolve()
                if p.is_relative_to(self.workspace) and p.is_dir():
                    if self.safety_policy.check_path(str(p)).allowed:
                        try:
                            entries = [entry.name for entry in p.iterdir() if self.safety_policy.check_path(str(entry)).allowed]
                            resolved[match] = "\n".join(entries)
                        except Exception as e:
                            resolved[match] = f"Error reading directory: {e}"
            elif match == "@git:status":
                try:
                    res = subprocess.run(["git", "status", "--short"], cwd=self.workspace, capture_output=True, text=True, check=False)
                    resolved[match] = res.stdout
                except Exception as e:
                    resolved[match] = f"Error running git status: {e}"
            elif match == "@git:diff":
                try:
                    res = subprocess.run(["git", "diff"], cwd=self.workspace, capture_output=True, text=True, check=False)
                    resolved[match] = res.stdout
                except Exception as e:
                    resolved[match] = f"Error running git diff: {e}"
        return resolved
