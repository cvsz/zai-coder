# Toolsets Operations

Toolsets explicitly group safe operations for ZAI Coder subagents.

## Available Toolsets

- `read_only`: Core inspection, `ls`, `grep`, `cat` equivalents.
- `test`: Suite execution (`pytest`, `make test`).
- `build`: Compilation and bundle tasks.
- `patch`: File modification primitives.
- `operator`: Full control (requires explicit elevation).
- `locked_down`: No execution allowed.
- `research_local`: Bounded codebase indexing.
- `media_local`: Generation primitives via local adapters.
- `server_local`: Safe networking.

## Security Posture

High-risk toolsets (e.g. `operator`) are disabled by default. All commands must still clear the global `SafetyPolicy` regardless of the assigned toolset.
