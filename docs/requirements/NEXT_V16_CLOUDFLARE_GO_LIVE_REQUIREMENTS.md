# ZAI Coder Control Plane v16 — Cloudflare Go-Live Requirements

## Added in v16

- Cloudflare Tunnel installer plan.
- Cloudflare Access policy checklist.
- DNS record planner.
- Hostname validator.
- Tunnel config generator.
- Local-to-public go-live wizard.
- Preflight exposure scan.
- DNS rollback plan.
- Public health verification plan.
- Cloudflare go-live UI pages.
- Server route integration.
- Scripts and docs.

## Safety

- No public route before Cloudflare Access.
- Localhost-first origin.
- Tunnel credentials stay outside git.
- DNS rollback plan generated before go-live.
- Public API must challenge or reject unauthenticated access.
