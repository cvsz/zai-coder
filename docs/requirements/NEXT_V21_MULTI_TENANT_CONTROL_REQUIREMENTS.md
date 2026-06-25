# ZAI Coder Control Plane v21 — Multi-Tenant Control Requirements

## Added in v21

- Tenant/org/workspace runtime isolation.
- Tenant-scoped API keys.
- Tenant-scoped audit logs.
- Workspace quota enforcement.
- Per-tenant provider permissions.
- Tenant backup/export policy.
- Tenant onboarding wizard.
- Admin tenant dashboard.
- Cross-tenant access guard.
- Tenant migration plan.
- Tenant scripts/routes/docs/tests.

## Safety

- Cross-tenant access is denied by default.
- API keys are scoped to org/workspace.
- Tokens are hashed at rest.
- Tenant export excludes secrets.
- Demo creation requires `APPLY=1`.
