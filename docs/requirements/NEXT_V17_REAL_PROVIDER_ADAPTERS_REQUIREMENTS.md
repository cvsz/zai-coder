# ZAI Coder Control Plane v17 — Real Provider Adapters Requirements

## Added in v17

- Real GitHub adapter wrapper.
- Real Cloudflare adapter wrapper.
- Real Docker adapter wrapper.
- Real PostgreSQL runtime adapter.
- Provider environment validation.
- Provider permission checks.
- Provider dry-run/apply switch.
- Provider approval guard.
- Audit log for every provider operation.
- Provider UI pages/routes.
- Provider scripts and docs.

## Safety

- Dry-run by default.
- Apply requires approval ID.
- Apply requires provider environment validation.
- Apply requires provider permission.
- Audit log records allowed and blocked operations.
- Commands are returned for approved runner/manual execution rather than silently mutating.
