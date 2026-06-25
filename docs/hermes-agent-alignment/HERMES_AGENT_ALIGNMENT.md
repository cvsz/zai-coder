# Hermes Agent Alignment Notes for ZAI v50

This package incorporates safe architectural patterns learned from Hermes Agent documentation:

- closed learning loop as reviewable skill/memory artifacts
- persistent memory patterns without secret export
- portable skill documents
- explicit project context files
- MCP/toolset filtering with allowlists
- local, Docker, SSH, and remote backend planning
- checkpoints and rollback before risky operations
- command approval and authorization gates
- messaging gateway concepts for operator notifications
- scoped delegation for parallel workstreams

ZAI v50 keeps these patterns local-first, dry-run-first, and review-first.
