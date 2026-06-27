# ZAI Coder v0.1.4 (Draft)

## Automated Agent Runners Phase

ZAI Coder `v0.1.4` focuses primarily on expanding local orchestration logic without compromising the strict local-first safety guarantees.

### Features
- **Provider Routing & Plugin MCP**: Enables modular support for MCP context backends.
- **Subagent Delegation Core**: Runners can cleanly branch tasks and delegate to focused subagents.
- **Toolsets & Context Overhaul**: Safe loading for local file context (`.zai.md`) and precise toolset permissions.
- **Production Self-Queue**: Durable local task persistence via SQLite.
- **Checkpoints**: Rollback system primitives to recover clean states.
- **OpenAI-Compatible API**: Extends the local server interface to handle standard tool calls natively.

### Security
- **Safe Runner Policy Hardened**: Additional regex validations covering generic `git add .` and shell execution behaviors to ensure deterministic, auditable code modifications.
