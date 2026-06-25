# ZAI Coder Control Plane v7 — Monetization Core Requirements

## Added in v7

- Plan catalog.
- Subscription state model.
- Append-only credit ledger.
- Quota reservation/commit/release.
- Usage accounting.
- Local token bucket rate limiting.
- Billing event replay protection.
- Idempotency store.
- Reconciliation helper.
- Stripe sandbox adapter placeholder.
- Static monetization admin dashboard.

## Safety

- No live payment calls.
- No provider secrets in repository.
- No floating point money.
- Use integer cents for currency.
- Use integer credit units for quota/credits.
- Ledger is append-only.
- Billing event IDs are unique to prevent replay.
- Idempotency keys are required for mutation-style events.
- Dry-run-first for any provider integration.
