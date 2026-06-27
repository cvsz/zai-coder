from __future__ import annotations

from zai_coder.mcp.adapter import MCPConfig


def get_git_mcp_config() -> MCPConfig:
    return MCPConfig(
        server_id="git-history",
        transport="stdio",
        command="git",
        enabled=True
    )

def get_sqlite_mcp_config(db_path: str) -> MCPConfig:
    return MCPConfig(
        server_id="sqlite-inspector",
        transport="stdio",
        command="sqlite3",
        args=["-readonly", "-bail", db_path],
        enabled=True
    )

def get_http_rest_mcp_config(base_url: str) -> MCPConfig:
    return MCPConfig(
        server_id="http-rest",
        transport="http",
        url=base_url,
        enabled=True
    )
