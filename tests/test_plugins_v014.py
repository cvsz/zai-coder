from zai_coder.core.plugins import PluginManifest, PluginRegistry

def test_plugin_registry():
    registry = PluginRegistry()
    m1 = PluginManifest(
        plugin_id="my-mcp",
        name="My MCP",
        plugin_type="mcp_adapter",
        enabled=True,
        allowed_tools=["read_file", "list_dir"],
        blocked_tools=["write_file"]
    )
    registry.register(m1)
    
    # Not enabled -> blocked
    m2 = PluginManifest("disabled-plugin", "Disabled", "toolset", enabled=False)
    registry.register(m2)
    
    assert registry.is_tool_allowed("my-mcp", "read_file") is True
    assert registry.is_tool_allowed("my-mcp", "write_file") is False
    assert registry.is_tool_allowed("my-mcp", "execute") is False
    
    assert registry.is_tool_allowed("disabled-plugin", "any") is False

def test_plugin_wildcard():
    registry = PluginRegistry()
    m1 = PluginManifest("wildcard", "Wildcard", "toolset", enabled=True, allowed_tools=["*"])
    registry.register(m1)
    assert registry.is_tool_allowed("wildcard", "dangerous_tool") is True
