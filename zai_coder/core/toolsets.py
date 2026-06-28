from __future__ import annotations

from dataclasses import dataclass, field

@dataclass
class Toolset:
    id: str
    label: str
    description: str
    enabled_by_default: bool = False
    allowed_commands: list[str] = field(default_factory=list)
    blocked_commands: list[str] = field(default_factory=list)
    requires_integration: bool = False
    risk_level: str = "low" # low, medium, high

class ToolsetRegistry:
    def __init__(self):
        self.toolsets: dict[str, Toolset] = {}
        
    def register(self, toolset: Toolset):
        self.toolsets[toolset.id] = toolset
        
    def get(self, toolset_id: str) -> Toolset | None:
        return self.toolsets.get(toolset_id)
        
    def get_all(self) -> list[Toolset]:
        return list(self.toolsets.values())

def get_default_toolset_registry() -> ToolsetRegistry:
    reg = ToolsetRegistry()
    reg.register(Toolset("read_only", "Read Only", "Safe read-only operations", True, allowed_commands=["cat", "ls", "grep"]))
    reg.register(Toolset("test", "Test", "Test running capabilities", True, allowed_commands=["pytest", "make test"]))
    reg.register(Toolset("build", "Build", "Build capabilities", True, allowed_commands=["make build", "npm build"]))
    reg.register(Toolset("patch", "Patch", "Code patching capabilities", True, allowed_commands=["patch"], risk_level="medium"))
    reg.register(Toolset("operator", "Operator", "Full operator capabilities", False, risk_level="high"))
    reg.register(Toolset("locked_down", "Locked Down", "Completely restricted", True, blocked_commands=["*"]))
    reg.register(Toolset("research_local", "Local Research", "Local codebase research", True))
    reg.register(Toolset("media_local", "Local Media", "Local media generation", True))
    reg.register(Toolset("audio_local", "Local Audio", "Local audio streaming and generation", True, risk_level="medium"))
    reg.register(Toolset("server_local", "Local Server", "Local API server testing", True))
    reg.register(Toolset("git_history", "Git History", "MCP integration for Git log/history", True, requires_integration=True))
    reg.register(Toolset("sqlite_inspector", "SQLite Inspector", "MCP integration for SQLite introspection", True, requires_integration=True))
    reg.register(Toolset("http_rest", "HTTP REST", "MCP integration for HTTP REST API interaction", True, requires_integration=True))
    return reg
