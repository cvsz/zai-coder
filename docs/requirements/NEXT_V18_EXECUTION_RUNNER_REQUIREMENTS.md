# ZAI Coder Control Plane v18 — Execution Runner Requirements

## Added in v18

- Approved command runner.
- Provider operation queue.
- Apply execution journal.
- Command timeout policy.
- stdout/stderr capture.
- Rollback hook registry.
- Retry policy.
- Human approval dashboard.
- Execution audit timeline.
- Failed-operation recovery plan.
- Execution scripts/routes/docs/tests.

## Safety

- Dry-run-first.
- `apply=True` requires approval id.
- No shell execution.
- Command allowlist.
- Dangerous token/pattern blocking.
- Safe relative working directory only.
- Journal captures every run/blocked run.
