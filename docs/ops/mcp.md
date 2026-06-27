# MCP Adapter Foundation

ZAI Coder introduces an experimental foundation for Model Context Protocol (MCP) integrations.

## Core Principles

1. **Disabled by Default**: No external MCP servers are configured or enabled by default.
2. **Explicit Registration**: Servers must be explicitly defined and registered.
3. **No Secrets in Repo**: The adapter blocks registrations containing suspicious keywords (like `SECRET` or `TOKEN`) in command arguments.
4. **Strict Tool Filtering**: MCP tool executions are gated by the `PluginRegistry`, which requires an explicit allowlist.
5. **Redacted Logging**: Tool execution arguments are filtered prior to logging to ensure no secrets bleed into system logs.
