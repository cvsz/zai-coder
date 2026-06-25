# ZAI Coder Control Plane v11 — Production SaaS Core Requirements

## Added in v11

- Organizations.
- Workspaces.
- User accounts.
- Invitations.
- Membership roles.
- SaaS SQLite store.
- Role/permission policy.
- API key enforcement facade.
- Quota enforcement middleware.
- Billing dashboard wired to monetization plans.
- Usage dashboard.
- Audit dashboard.
- Admin settings dashboard.
- Integration audit log.
- Job retry policy.
- Database migrations CLI facade.
- Worker daemon facade.
- First-run setup wizard.
- Deployment wizard.
- SaaS route registry.
- Server route integration.
- OpenAPI SaaS path extension.

## Safety

- API key must be enforced for production routes.
- Least privilege role checks.
- Quota check before expensive actions.
- Integration actions audit-loggable.
- Dry-run-first external integrations remain required.
- No public unauthenticated SaaS admin endpoints in production.
