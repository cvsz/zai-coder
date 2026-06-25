# ZAI Coder Control Plane v19 — Observability Suite Requirements

## Added in v19

- Metrics registry.
- Prometheus-style metrics endpoint.
- Structured event bus.
- Alert rules.
- Health trend snapshots.
- Execution/provider dashboards.
- Log retention policy.
- Incident report generator.
- SLO/SLA templates.
- Uptime verification plan.
- Observability scripts/routes/docs/tests.

## Safety

- No external telemetry upload by default.
- Metrics are local/exportable.
- Logs retention excludes secret and generated-heavy paths.
- Incident reports avoid secret capture.
- Public endpoint expectations include Access challenge or 401/403 for protected APIs.
