# IDE Integration Plan

ZAI Coder is designed to be environment-agnostic, running safely via CLI, TUI, and eventually directly inside IDEs.

## Integration Status

- **available**: Local server primitives (API endpoints used by CLI/TUI).
- **planned**: ACP-compatible editors (e.g., editors supporting the Agent Context Protocol).
- **requires_integration**: VS Code extensions, Zed integrations, JetBrains plugin adapters.

## Guardrails

- Integration via an IDE must not bypass the core `SafetyPolicy`.
- File system access requested by an IDE extension must still be scoped to the workspace bounds.
