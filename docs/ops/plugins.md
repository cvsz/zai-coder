# Plugin System Foundation

ZAI Coder incorporates a foundational plugin registry that allows extending behavior (like toolsets, memory providers, and MCP adapters) safely.

## Safety Guidelines

- Plugins are **disabled by default**.
- Plugins must specify explicitly what tools they allow or block.
- Credentials and real API keys must never be stored in git or manifest files.
- All tools invoked through plugins are routed through the core `SafetyPolicy`.
