# ZAI Coder Control Plane v28 — Plugin Connector Hub Requirements

## Added in v28

- Connector catalog.
- Connector manifest validator.
- Env/secret guard.
- Tenant-scoped connector permissions.
- Install/enable policy.
- Dry-run sync plans.
- Webhook ingress scaffold.
- Provider adapter stubs.
- Connector dashboard.
- Connector audit log.
- Offline import/export.
- Connector scripts/routes/docs/tests.

## Safety

- Local-first and dry-run-first.
- No external connector API calls.
- Demo install/enable requires `APPLY=1`.
- Secrets are redacted in env reports.
- Live secret env keys are blocked.
- Connector webhooks are scaffold-only.
