# Clean Release Audit Report

Date: 2026-06-26

## Scope

- Audited local source tree under `/home/zeazdev/zai-coder`.
- No deploy, push, merge, publish, or external mutation was performed.
- Root `.git/` was preserved for source-control integrity and excluded from the release archive.

## Artifact Cleanup

- Removed generated Python cache directories and `*.pyc` files found under `zai_coder/`.
- Removed local runtime SQLite files under `data/`.
- Removed untracked nested duplicate shell helper tree at `scripts/git/git/`.
- `.pytest_cache/` was included in cleanup if present.

## Secret Findings

- Reviewed `reports/SECRET_FINDINGS_REDACTED.tsv`.
- Secret-like values remain redacted.
- No raw secret value is included in this report.

## Shell Risk Findings

- Reviewed `reports/SHELL_RISK_FINDINGS.tsv`.
- `merge-zai-zips.sh` destructive merge cleanup is marked manual-only.
- `Makefile clean-safe` cleanup is marked local-only and `APPLY=1` gated.
- `scripts/safety-dry-run.sh` broad `rm -rf` handling is disabled by default and blocks dangerous patterns.
- `Makefile gpg-push` is manual-only and disabled by default.

## Python Risk Findings

- Reviewed `reports/PYTHON_RISK_FINDINGS.tsv`.
- Local SQLite `executescript` findings are static schema initialization for local audit logs.
- Provider operation routes remain dry-run by default and require explicit apply plus approval context before returning an apply-permitted plan.
- Provider executor does not execute provider commands directly; approved apply returns a manual execution plan.
- One stale Python finding references a file not present in the audited tree and is marked as stale.

## Shell Permissions

- Intended executable entrypoints are shell scripts under `scripts/`, `run.sh`, `install.sh`, `merge-zai-zips.sh`, and `zai-coder`.
- `zai-coder` is executable and has a shebang.
- `deploy/logrotate/zai-coder` is not executable and does not require a shebang because it is a logrotate config.

## Release Archive

- Release archive: `zai-coder-clean-release.tgz`
- Checksum file: `zai-coder-clean-release.sha256`
- Archive excludes `.git/`, `.env`, Python caches, pytest caches, generated `out/` artifacts, local DB files, and prior archive/checksum outputs.

## Validation Commands

- `python3 -m pytest -q`
- `./run.sh doctor`
- `make safety-check`
- `make final-release-status || true`

- `python3 -m pytest -q`: passed, 341 tests; 2 existing warnings.
- `./run.sh doctor`: exited 0; Ollama binary found, local socket check reported sandbox permission denial.
- `make safety-check`: exited 0 as default dry-run.
- `make safety-check APPLY=1`: passed local safety scan; warnings were generated/noisy local artifact paths.
- `make final-release-status || true`: exited 0 as default dry-run.
- `make final-release-status APPLY=1`: passed local final release status.
