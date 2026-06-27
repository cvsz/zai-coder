import pytest
from zai_coder.core.plugins import PluginRegistry, PluginManifest
from zai_coder.core.safety import SafetyPolicy
from zai_coder.mcp.adapter import MCPAdapter, MCPConfig

def test_mcp_adapter_registration():
    registry = PluginRegistry()
    safety = SafetyPolicy()
    adapter = MCPAdapter(registry, safety)
    
    # Valid config
    adapter.register_server(MCPConfig("s1", "stdio", command="python3 server.py"))
    assert "s1" in adapter.configs
    
    # Blocked config (secret in command)
    adapter.register_server(MCPConfig("s2", "stdio", command="python3 server.py --token SECRET_123"))
    assert "s2" not in adapter.configs

def test_mcp_adapter_execution_blocked():
    registry = PluginRegistry()
    safety = SafetyPolicy()
    adapter = MCPAdapter(registry, safety)
    
    adapter.register_server(MCPConfig("s1", "stdio", enabled=True))
    
    # Blocked because plugin not registered
    res = adapter.execute_tool_dry_run("s1", "read_file", {})
    assert "not allowed by registry" in res["error"]
    
def test_mcp_adapter_execution_allowed():
    registry = PluginRegistry()
    registry.register(PluginManifest("s1", "S1", "mcp_adapter", enabled=True, allowed_tools=["read_file"]))
    
    safety = SafetyPolicy()
    adapter = MCPAdapter(registry, safety)
    adapter.register_server(MCPConfig("s1", "stdio", enabled=True))
    
    res = adapter.execute_tool_dry_run("s1", "read_file", {"path": "test.txt", "my_secret": "hidden"})
    
    assert "error" not in res
    assert res["status"] == "simulated"
    assert res["redacted_args"]["path"] == "test.txt"
    assert res["redacted_args"]["my_secret"] == "***"
