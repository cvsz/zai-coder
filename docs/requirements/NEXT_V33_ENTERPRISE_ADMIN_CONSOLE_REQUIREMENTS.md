# ZAI Coder Control Plane v33 — Enterprise Admin Console Requirements

## Added in v33

- Enterprise admin dashboard.
- Tenant/org/workspace/user directory.
- RBAC role matrix and assignment policy.
- Feature flag catalog and change plans.
- Redacted config registry.
- Service control panel plans.
- Support access/impersonation guard.
- Unified audit explorer.
- Safe admin export bundle.
- Admin audit log.
- Admin-console scripts/routes/docs/tests.

## Safety

- Read-only previews by default.
- No direct service mutations.
- Demo exports/actions require `APPLY=1`.
- Secrets are redacted.
- Support access requires approval and is time-bound.
- Service action plans are dry-run only.
