# ZAI Coder Control Plane v25 — Worker Orchestration Requirements

## Added in v25

- Worker registry.
- Job queue.
- Lease and heartbeat support.
- Scheduler manifest and fire plans.
- Retry and dead-letter policy.
- Concurrency limits.
- Tenant-scoped worker guard.
- Execution-runner bridge.
- Worker dashboard.
- Worker audit log.
- Worker scripts/routes/docs/tests.

## Safety

- Workers do not execute shell directly.
- Execution bridge uses v18 approved command runner specs.
- Demo mutations require `APPLY=1`.
- Tenant-scoped workers can only process matching tenant jobs.
- Shared workers must still pass tenant guard.
