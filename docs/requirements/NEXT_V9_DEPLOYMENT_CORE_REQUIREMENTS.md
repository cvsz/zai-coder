# ZAI Coder Control Plane v9 — Deployment Core Requirements

## Added in v9

- Dependency-light local HTTP server.
- Healthcheck endpoint.
- API status endpoint.
- Static dashboard serving.
- API auth middleware foundation.
- Backup/restore helpers.
- Admin bootstrap command.
- Cloudflare tunnel config generator.
- Release artifact builder.
- SHA256 checksum manifest.
- Minimal SBOM generator.
- Production systemd service template.
- Docker Compose production profile.
- Logrotate config.
- Deployment scripts and tests.

## Commands

```bash
make serve-local
make health-demo
make backup-plan
make backup-create APPLY=1
make admin-bootstrap
make admin-bootstrap APPLY=1 ADMIN_EMAIL=admin@example.com
make cloudflare-generate-config HOSTNAME=zai.zeaz.dev
make release-plan
make release-build APPLY=1
make release-checksums
make release-sbom
```

## Safety

- localhost-first.
- API key required before public exposure.
- Cloudflare Access recommended.
- No secrets in repo.
- Backup before migrations.
- Release builder excludes caches, generated artifacts, `.env`, and `apps/zlms/**`.
