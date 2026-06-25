# Runbook — Monetization Core

## Purpose

Manage local plan metadata, subscriptions, quota, credit ledger, usage accounting, and reconciliation.

## Flow

1. Select plan.
2. Create local subscription.
3. Grant included credits.
4. Reserve quota before action.
5. Commit quota after success or release after failure.
6. Record usage event.
7. Reconcile periodically.

## Safety

- No live payment calls.
- No secrets in repository.
- Use idempotency keys.
- Keep ledger append-only.
- Store money in integer cents.
- Store credits in integer units.
