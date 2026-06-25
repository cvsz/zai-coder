# Runbook — Deployment Core

## Preflight

```bash
python3 -m pytest -q
make deployment-core
make health-demo
make cloudflare-checklist
```

## Local serve

```bash
make serve-local
```

Open:

```text
http://127.0.0.1:8765
http://127.0.0.1:8765/healthz
```

## Backup

```bash
make backup-plan
make backup-create APPLY=1
```

## Admin bootstrap

```bash
make admin-bootstrap
make admin-bootstrap APPLY=1 ADMIN_EMAIL=admin@example.com
```

The raw API key is shown once. Do not commit it.

## Cloudflare

```bash
make cloudflare-generate-config HOSTNAME=zai.zeaz.dev TUNNEL_NAME=zai-coder
```

Review generated config. Do not commit credentials.

## Release artifacts

```bash
make release-plan
make release-build APPLY=1
make release-checksums
make release-sbom
```
