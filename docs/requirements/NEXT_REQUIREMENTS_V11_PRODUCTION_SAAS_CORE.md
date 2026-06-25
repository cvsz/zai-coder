# ZAI Coder v11 — Production SaaS Core Requirements

## Target

`zai-coder-control-plane-v11-production-saas-core.zip`

## Scope

Move from deployable local app to production SaaS control plane.

## Add next

- organizations
- workspaces
- users
- invitations
- roles and permissions wired into API
- API key middleware fully enforced
- quota enforcement middleware
- billing dashboard wired to monetization core
- usage dashboard
- audit dashboard
- admin settings UI
- OpenAPI route coverage
- database migrations CLI
- background worker daemon command
- job retry policy
- integration audit log
- deployment wizard
- first-run setup wizard

## Safety

- no public unauthenticated endpoints
- least privilege roles
- audit every mutation
- quota checks before expensive actions
- dry-run-first for external integrations
