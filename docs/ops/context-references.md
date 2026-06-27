# Context References

Users can explicitly include local resources into agent contexts using `@` tags.

## Supported Tags

- `@file:path/to/file` - Read a specific local file.
- `@dir:path/to/dir` - Read the directory listing.
- `@git:status` - Outputs `git status --short`.
- `@git:diff` - Outputs `git diff`.

## Guardrails

- All references are subject to the `SafetyPolicy` path filtering.
- Resolution fails safely if the target is outside the workspace or blocked.
- Remote fetching (e.g. `@url`) is explicitly deferred until network boundaries are defined.
