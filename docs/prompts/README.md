# ZAI Coder Prompt Pack

This directory stores reusable operational prompts for the next ZAI Coder phases after the v0.1.3 release, generated-state guardrails, and release-process guardrails.

## Current Baseline

- Repository: `cvsz/zai-coder`
- Current stable release: `v0.1.3`
- Current package version: `0.1.3`
- Latest verified guardrail PRs:
  - PR #21: generated-state guardrails
  - PR #22: release-process guardrails
- Release posture:
  - Signed tag is preserved.
  - GitHub release is published.
  - Release assets are not mutated by these prompts.
  - Future release work should be PR-first and audit-safe.

## Prompt Order

1. `00-release-ledger.md` — current release and process ledger.
2. `01-v014-planning.md` — create v0.1.4 planning baseline.
3. `02-pr23-merge-gate.md` — review and merge the v0.1.4 planning PR.
4. `03-cli-diagnostics.md` — implement CLI operator diagnostics.
5. `04-safe-runner-policy.md` — harden safe-runner and policy coverage.
6. `05-installer-reliability.md` — improve installer/update/uninstall reliability.
7. `06-release-readiness.md` — add release readiness status and precondition checks.
8. `07-operator-docs.md` — polish operator documentation and examples.
9. `08-server-api-diagnostics.md` — optional server/API diagnostics phase.
10. `09-v014-final-readiness.md` — prepare final readiness docs for v0.1.4.
11. `10-v014-release-candidate.md` — prepare the v0.1.4 release candidate.
12. `11-v014-publish.md` — publish v0.1.4 after candidate merge.
13. `12-post-release-verification.md` — post-release verification and cleanup.

## Universal Safety Rules

All prompts in this directory inherit these rules:

- Do not rewrite history.
- Do not force push.
- Do not push directly to `main`.
- Do not use `git add .`.
- Do not use `git add -A`.
- Do not use `--no-verify`.
- Do not commit `dist/`, `.zai-coder/`, `.pytest_cache/`, runtime DBs, SQLite files, generated evidence/export JSON, `status.txt`, or runtime logs.
- No version bump unless the prompt explicitly says it is a release-candidate phase.
- No tag, GitHub release, or asset upload unless the prompt explicitly says it is a publish phase.
- Stage exact files only.
- Prefer small PRs with merge commits for audit trail.

## Expected Validation Baseline

After PR #22, expected validation is approximately:

```bash
python3 -m pytest -q
# expected: 477 passed

make repo-check
make secret-scan
make stage-manifest-check
./scripts/repo/check-generated-state.sh
./scripts/repo/check-ci-pytest-setup.sh
```
