# ZAI Coder v0.1.1 Release Notes

- **Release Type**: Patch
- **Previous Release**: v0.1.0 at `b6b09e3`
- **Base Post-Merge Commit**: `4cced4b`

## Key Changes
- PR #4 enterprise hardening merged
- Local server implementation added
- Migrations/update framework added
- Repository readiness checks hardened
- Secret scanning improved
- Safety/registry/test coverage expanded
- Script executable permissions normalized
- Generated runtime state ignored

## Compatibility
- Local-first design preserved
- Python stdlib-first design preserved
- No mandatory network dependency

## Known Warnings
- Existing pytest warnings remain non-blocking

## Upgrade Notes
- Pull latest main after release
- Reinstall package if using local install
- Do not reuse generated local DB/cache files between environments
