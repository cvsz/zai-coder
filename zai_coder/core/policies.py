import json
import re
from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, Any, List

@dataclass
class PolicyProfile:
    name: str
    allowed_command_roots: list[str] = field(default_factory=list)
    denied_patterns: list[str] = field(default_factory=list)
    protected_paths: list[str] = field(default_factory=list)
    generated_paths: list[str] = field(default_factory=list)
    max_timeout: int = 180
    require_approval: bool = True
    allow_network: bool = False

    def check_command(self, command: str) -> tuple[bool, str]:
        cmd_root = command.split()[0] if command.split() else ""
        if "*" not in self.allowed_command_roots and cmd_root not in self.allowed_command_roots:
            return False, f"Command root '{cmd_root}' not allowed by profile '{self.name}'"
        for pattern in self.denied_patterns:
            if re.search(pattern, command):
                return False, f"Command matches denied pattern: {pattern}"
        return True, "OK"

    def check_path(self, path: str) -> tuple[bool, str]:
        p = path.replace("\\", "/")
        for protected in self.protected_paths:
            if protected in p or p.startswith(protected):
                return False, f"Path protected by profile: {protected}"
        for generated in self.generated_paths:
            if generated in p or p.startswith(generated):
                return False, f"Generated path access blocked: {generated}"
        return True, "OK"

class PolicyManager:
    def __init__(self, workspace: str = "."):
        self.workspace = Path(workspace).expanduser().resolve()
        self.policies: Dict[str, PolicyProfile] = {}
        self._load_defaults()
        self._load_from_assets()

    def _load_defaults(self):
        common_denied = [
            r"\bgit\s+add\s+\.(?:$|\s)",
            r"\bgit\s+add\s+-A(?:$|\s)",
            r"--no-verify\b",
            r"\bgit\s+push\b.*\s(-f|--force|--force-with-lease)\b",
            r"\brm\s+-rf\s+(/|~|\$HOME|\.)($|\s)",
            r"\bsudo\s+rm\s+-rf\b",
            r"\bchmod\s+-R\s+777\b",
            r";\s*bash", r";\s*sh", r"\|\s*bash", r"\|\s*sh",
            r"\$\(", r"`.*`", r"base64\s+-d\s*\|"
        ]
        common_protected = ["apps/zlms/"]
        common_generated = ["node_modules/", "dist/", ".next/", "coverage/", "reports/", ".turbo/", ".vite/", "vendor/ai-assets/"]

        self.policies["read_only"] = PolicyProfile(
            name="read_only",
            allowed_command_roots=["ls", "cat", "grep", "find", "head", "tail", "git"],
            denied_patterns=common_denied,
            protected_paths=common_protected,
            generated_paths=common_generated,
            max_timeout=60,
            require_approval=False,
            allow_network=False
        )
        
        self.policies["developer"] = PolicyProfile(
            name="developer",
            allowed_command_roots=["ls", "cat", "grep", "find", "pytest", "python", "python3", "make", "npm", "yarn", "git", "echo", "rm", "mkdir"],
            denied_patterns=common_denied,
            protected_paths=common_protected,
            generated_paths=common_generated,
            max_timeout=300,
            require_approval=False,
            allow_network=True
        )

        self.policies["release"] = PolicyProfile(
            name="release",
            allowed_command_roots=["make", "npm", "yarn", "git", "python", "python3", "zip", "tar"],
            denied_patterns=common_denied,
            protected_paths=common_protected,
            generated_paths=common_generated,
            max_timeout=600,
            require_approval=True,
            allow_network=True
        )

        self.policies["operator"] = PolicyProfile(
            name="operator",
            allowed_command_roots=["*"],
            denied_patterns=common_denied,
            protected_paths=[],
            generated_paths=[],
            max_timeout=3600,
            require_approval=True,
            allow_network=True
        )

        self.policies["locked_down"] = PolicyProfile(
            name="locked_down",
            allowed_command_roots=[],
            denied_patterns=[".*"],
            protected_paths=["/"],
            generated_paths=["/"],
            max_timeout=0,
            require_approval=True,
            allow_network=False
        )

    def _load_from_assets(self):
        assets_dir = self.workspace / "assets" / "policies"
        if not assets_dir.exists():
            return
            
        for path in assets_dir.glob("*.json"):
            try:
                data = json.loads(path.read_text())
                name = path.stem
                self.policies[name] = PolicyProfile(
                    name=name,
                    allowed_command_roots=data.get("allowed_command_roots", []),
                    denied_patterns=data.get("denied_patterns", []),
                    protected_paths=data.get("protected_paths", []),
                    generated_paths=data.get("generated_paths", []),
                    max_timeout=data.get("max_timeout", 180),
                    require_approval=data.get("require_approval", True),
                    allow_network=data.get("allow_network", False)
                )
            except Exception:
                pass

    def get_profile(self, name: str) -> PolicyProfile:
        return self.policies.get(name, self.policies["locked_down"])

    def list_profiles(self) -> list[str]:
        return list(self.policies.keys())
