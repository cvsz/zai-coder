---
name: add-new-module-with-tests
description: Workflow command scaffold for add-new-module-with-tests in zai-coder.
allowed_tools: ["Bash", "Read", "Write", "Grep", "Glob"]
---

# /add-new-module-with-tests

Use this workflow when working on **add-new-module-with-tests** in `zai-coder`.

## Goal

Implements a new core module or subsystem along with corresponding unit/integration tests.

## Common Files

- `zai_coder/core/*.py`
- `zai_coder/server/*.py`
- `zai_coder/migrations/__init__.py`
- `tests/test_*.py`

## Suggested Sequence

1. Understand the current state and failure mode before editing.
2. Make the smallest coherent change that satisfies the workflow goal.
3. Run the most relevant verification for touched files.
4. Summarize what changed and what still needs review.

## Typical Commit Signals

- Create new implementation files in zai_coder/core/ or zai_coder/server/ or similar module directory.
- Add corresponding test files in tests/ (e.g., tests/test_<module>.py).
- Update __init__.py if exposing new imports or package namespaces.

## Notes

- Treat this as a scaffold, not a hard-coded script.
- Update the command if the workflow evolves materially.