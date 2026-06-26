import json
from pathlib import Path
from zai_coder.core.policy import PolicyProfile

# Fallback definitions
FALLBACK_POLICIES = {
    "read_only": PolicyProfile(
        name="read_only",
        description="Fallback read_only",
        allowed_commands=["ls", "cat", "grep"],
        denied_patterns=["rm -rf", "sudo", "chmod", "git add", "git commit", "git push"],
        protected_paths=["apps/zlms/"],
        generated_paths=["node_modules/", "dist/"],
        max_timeout_seconds=60,
        require_approval=False,
        allow_network=False,
        allow_shell=False,
        allow_write=False
    ),
    "developer": PolicyProfile(
        name="developer",
        description="Fallback developer",
        allowed_commands=["ls", "cat", "grep", "pytest", "python", "make", "git"],
        denied_patterns=["rm -rf /", "sudo rm -rf"],
        protected_paths=["apps/zlms/"],
        generated_paths=["node_modules/", "dist/"],
        max_timeout_seconds=300,
        require_approval=False,
        allow_network=True,
        allow_shell=False,
        allow_write=True
    )
}

class PolicyLoader:
    def __init__(self, assets_dir: str | Path = "assets/policies"):
        self.assets_dir = Path(assets_dir)
        
    def list_policies(self) -> list[str]:
        if not self.assets_dir.exists():
            return list(FALLBACK_POLICIES.keys())
        return [p.stem for p in self.assets_dir.glob("*.json")]
        
    def load(self, name: str) -> PolicyProfile:
        path = self.assets_dir / f"{name}.json"
        if not path.exists():
            if name in FALLBACK_POLICIES:
                return FALLBACK_POLICIES[name]
            raise ValueError(f"Policy '{name}' not found")
            
        try:
            with path.open("r", encoding="utf-8") as f:
                data = json.load(f)
            return PolicyProfile(**data)
        except Exception as e:
            if name in FALLBACK_POLICIES:
                return FALLBACK_POLICIES[name]
            raise ValueError(f"Failed to load policy '{name}': {e}")
