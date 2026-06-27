from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

@dataclass
class PluginManifest:
    plugin_id: str
    name: str
    plugin_type: str # toolset, hook, memory_provider, context_engine, mcp_adapter
    enabled: bool = False
    risk_level: str = "low" # low, medium, high
    allowed_tools: list[str] = field(default_factory=list)
    blocked_tools: list[str] = field(default_factory=list)
    config_schema: dict[str, Any] = field(default_factory=dict)

class PluginRegistry:
    def __init__(self):
        self.plugins: dict[str, PluginManifest] = {}

    def register(self, manifest: PluginManifest):
        self.plugins[manifest.plugin_id] = manifest

    def get_plugin(self, plugin_id: str) -> PluginManifest | None:
        return self.plugins.get(plugin_id)

    def is_tool_allowed(self, plugin_id: str, tool_name: str) -> bool:
        plugin = self.get_plugin(plugin_id)
        if not plugin or not plugin.enabled:
            return False
            
        if tool_name in plugin.blocked_tools:
            return False
            
        if not plugin.allowed_tools or "*" in plugin.allowed_tools:
            return True
            
        return tool_name in plugin.allowed_tools
