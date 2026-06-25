# ZAI Coder Control Plane v22 — Billing Usage Enforcement Requirements

## Added in v22

- Tenant billing account model.
- Usage event ledger.
- Workspace usage aggregation.
- Billing plans.
- Quota-to-plan enforcement.
- Trial/free/pro/enterprise plan policy.
- Invoice draft generator.
- Overage alert policy.
- Usage dashboard.
- Billing audit trail.
- Billing scripts/routes/docs/tests.

## Safety

- No real payment capture.
- Invoice generation is draft-only.
- Usage mutation demo requires `APPLY=1`.
- Billing tokens/secrets are not stored.
- Billing audit events are tenant-scoped.
