from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any

from zai_coder.core.plugins import PluginRegistry
from zai_coder.core.safety import SafetyPolicy

logger = logging.getLogger(__name__)

@dataclass
class MCPConfig:
    server_id: str
    transport: str # "stdio" or "http"
    command: str | None = None
    url: str | None = None
    enabled: bool = False
    args: list[str] | None = None

class MCPAdapter:
    def __init__(self, registry: PluginRegistry, safety: SafetyPolicy):
        self.registry = registry
        self.safety = safety
        self.configs: dict[str, MCPConfig] = {}
        
    def register_server(self, config: MCPConfig):
        # Prevent secret injection via command strings
        if config.command and ("SECRET" in config.command.upper() or "TOKEN" in config.command.upper()):
            logger.warning(f"Rejected MCP config for {config.server_id}: possible secret in command")
            return
        self.configs[config.server_id] = config

    def execute_tool_dry_run(self, server_id: str, tool_name: str, args: dict[str, Any]) -> dict[str, Any]:
        config = self.configs.get(server_id)
        if not config:
            return {"error": f"Server {server_id} not registered."}
            
        if not config.enabled:
            return {"error": f"Server {server_id} is disabled."}
            
        # Check plugin registry bounds
        if not self.registry.is_tool_allowed(server_id, tool_name):
            return {"error": f"Tool {tool_name} is not allowed by registry for server {server_id}."}
            
        # All tools must also pass SafetyPolicy check implicitly or explicitly depending on tool semantic
        # For this foundation, we just log redacted metadata
        redacted_args = {k: "***" if "secret" in k.lower() else v for k, v in args.items()}
        
        logger.info(f"[MCP] Dry-run execution of {tool_name} on {server_id} with args {redacted_args}")
        
        return {
            "status": "simulated",
            "server_id": server_id,
            "tool_name": tool_name,
            "redacted_args": redacted_args
        }
