# ZAI Coder Control Plane v14 — Deploy Installer Requirements

## Added in v14

- Ubuntu 24.04 installer.
- One-command setup script.
- `.env.example` generator.
- Local deploy script.
- Docker Compose production launcher.
- Systemd install/apply script.
- Cloudflare Tunnel/Access plan.
- First-run admin bootstrap plan.
- Healthcheck script.
- Backup/restore scripts.
- Upgrade/rollback scripts.
- Go-live checklist.
- Deployment installer core modules.
- Deployment docs and operation docs.
- Production installer tests.

## Safety

- Dry-run-first.
- `APPLY=1` required for mutation.
- Localhost-first.
- Cloudflare Access before public exposure.
- Backup before migration/upgrade/restore.
- No committed secrets.
