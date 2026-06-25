# ZAI Coder Control Plane v26 — Agent Runtime Supervisor Requirements

## Added in v26

- Agent registry.
- Lifecycle supervisor.
- Heartbeat monitor.
- Sandbox profile policy.
- Task assignment store.
- Budget guard.
- Permission guard.
- Crash recovery plan.
- Worker orchestration bridge.
- Agent dashboard.
- Agent audit log.
- Agent scripts/routes/docs/tests.

## Safety

- Agents do not launch arbitrary processes.
- Runtime execution is bridged through worker orchestration and approved execution specs.
- Demo mutations require `APPLY=1`.
- Sandbox blocks secrets, repo internals, and `apps/zlms/`.
- Budget and permission gates are checked before start.
