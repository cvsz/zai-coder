from dataclasses import dataclass, field
import re

@dataclass
class PolicyProfile:
    name: str
    description: str
    allowed_commands: list[str] = field(default_factory=list)
    denied_patterns: list[str] = field(default_factory=list)
    protected_paths: list[str] = field(default_factory=list)
    generated_paths: list[str] = field(default_factory=list)
    max_timeout_seconds: int = 60
    require_approval: bool = False
    allow_network: bool = False
    allow_shell: bool = False
    allow_write: bool = False
    
    _compiled_patterns: list[re.Pattern] = field(init=False, repr=False)
    
    def __post_init__(self):
        self._compiled_patterns = [re.compile(p) for p in self.denied_patterns]
        
    def check_command(self, command: str) -> tuple[bool, str]:
        normalized = command.strip()
        for p, raw in zip(self._compiled_patterns, self.denied_patterns):
            if p.search(normalized):
                return False, f"Command matches denied pattern: {raw}"
        return True, "OK"
        
    def check_path(self, path: str) -> tuple[bool, str]:
        p = path.replace("\\", "/")
        for protected in self.protected_paths:
            if p.startswith(protected) or protected in p:
                return False, f"Path is protected: {protected}"
        for generated in self.generated_paths:
            if p.startswith(generated) or generated in p:
                return False, f"Path is generated: {generated}"
        return True, "OK"
