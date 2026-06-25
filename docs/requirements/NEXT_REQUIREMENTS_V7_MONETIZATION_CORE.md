# ZAI Coder v7 — Monetization Core Requirements

## Target

`zai-coder-control-plane-v7-monetization-core.zip`

## Scope

Add billing, quota, credits, teams, subscriptions, usage accounting, and product packaging.

## Requirements

### Billing

- product plans
- subscription states
- invoice records
- payment provider adapters
- no live payment calls by default
- sandbox-first

### Quota

- usage counters
- reservation/commit/release model
- idempotency keys
- audit logs
- local SQLite first
- future Postgres adapter

### Credits

- append-only ledger
- BigInt integer units
- no floating point money
- reconciliation command
- billing event replay protection

### SaaS Packaging

- plan definitions
- team member limits
- workspace limits
- agent run limits
- media generation limits
- API rate limits

### Admin UI

- plan management
- team usage dashboard
- quota dashboard
- audit dashboard
- billing event log

## Safety

- no real payment mutation without explicit adapter credentials
- no secret storage in repo
- dry-run-first
- full audit log
