# Claude Code Feature Coverage

This matrix tracks Claude Code-style capabilities as product claims for ZAI Coder. It separates implemented local features from partial foundations, planned work, and provider-dependent integration work.

## Status meanings

- `available`: implemented locally and safe to claim.
- `partial`: usable foundation exists, but product copy must be cautious.
- `planned`: not implemented yet.
- `requires_integration`: needs external provider, API, OAuth, MCP, browser service, IDE protocol, or credentials.
- `do_not_claim`: unsupported claim.

## Coverage

| Feature | Status | Notes |
|---|---|---|
| Terminal CLI | available | `zai_coder/cli.py` |
| File read/write/edit | partial | Patch and repair flows exist; broader editor parity is planned. |
| Safe shell runner | available | `SafetyPolicy` and `ToolRuntime` guard commands. |
| Glob/search | partial | Local index/search foundations exist. |
| Task planning | available | Multi-agent plan command exists. |
| Persistent memory | partial | Local memory exists; CLAUDE.md-style parity is planned. |
| Project instructions | partial | AGENTS/prompts exist; CLAUDE.md parity is planned. |
| Slash commands | planned | Needs reusable command registry. |
| Custom commands | planned | Needs repo-defined command packs. |
| Hooks | planned | Needs deterministic lifecycle runner. |
| Subagents | partial | Agent runtime supervisor and queue foundations exist. |
| Skills | partial | Skill catalogs and marketplace foundations exist. |
| MCP | requires_integration | Needs configured MCP servers and credentials. |
| Permissions | available | Safety policy gates command/path access. |
| Sessions | partial | Local session module exists; full resume UX is planned. |
| Checkpointing | partial | Patch checkpoints exist; rollback product flow is planned. |
| IDE integration | planned | Needs editor protocol integration. |
| SDK/headless | partial | CLI/Python modules are callable; formal SDK is planned. |
| Plugins | partial | Plugin and connector catalogs exist; remote install needs integration. |
| Web search/fetch | requires_integration | Needs provider/browser/MCP service. |
| Background monitor | partial | Local monitor exists; event-stream parity is planned. |
| Artifacts | available | Local artifact registry with hashes and JSON export exists. |
| Output styles | planned | Needs prompt/style registry. |
| Enterprise settings | partial | Policy/admin foundations exist; managed policy parity is planned. |

