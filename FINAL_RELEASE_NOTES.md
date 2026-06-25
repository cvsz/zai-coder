# Final Release Notes

## Summary
The ZAI Coder Control Plane v50-final-enterprise-release is a local-first, source-safe enterprise-ready release.

## Included Modules
Full monorepo implementation (v1-v50).

## Safety Model
Local-first development with dry-run-first enforcement; manual approval required for all mutations; secret-redaction enforced via GitOps/CLI.

## Install Instructions
1. Prepare environment: `cp .env.example .env` and populate variables.
2. Setup environment: `mkdir -p .zai-coder/logs .zai-coder/cache .zai-coder/tmp .zai-coder/checkpoints`
3. Run install: `SOURCE_DIR="..." PREFIX="..." APPLY=1 ./install.sh`

## Dry-Run Instructions
1. Always run `make dry-run` to preview operations.
2. Use `APPLY=0` (default) for all commands that support it.

## Local Validation
- `python3 -m pytest -q`
- `make safety-check`
- `make final-release-status`

## Manual-Only Release/Push
Use `make gpg-commit` and `make gpg-push` (if enabled) manually.

## Rollback Instructions
See `docs/runbooks/rollback-procedure.md`.

## Known Warnings
- Ollama socket sandbox permission denial.
- Pytest warnings (collection, return type).
