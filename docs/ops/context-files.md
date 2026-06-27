# Context Files Operations

ZAI Coder supports auto-discovering project context files in the root workspace.

## Supported Formats

- `.zai.md`
- `.hermes.md`
- `AGENTS.md`
- `CLAUDE.md`
- `SOUL.md`
- `.cursorrules`

## Loading Mechanics

Files are only loaded if they exist, pass the `SafetyPolicy`, and are under 100KB in size. Content is automatically appended to the agent's system prompt or available as RAG context during operations.
