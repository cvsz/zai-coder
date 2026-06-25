# Production Hardening Guide

## Install runtime dependencies

```bash
python3 -m pip install -r requirements-production.txt
```

## Run migrations

```bash
make production-migrate-plan
make production-migrate-apply APPLY=1
```

## Serve locally

```bash
make serve-fastapi
```

## Docker

```bash
docker compose -f deploy/docker/docker-compose.production-hardening.yml config
docker compose -f deploy/docker/docker-compose.production-hardening.yml up --build
```

## Cloudflare

Read:

```text
deploy/cloudflare/cloudflare-access-production.md
```

## Production rules

- Bind app to localhost first.
- Use Cloudflare Access or equivalent identity control.
- Keep secrets in environment or secret manager only.
- Run backups and restore tests.
- Monitor health and logs.
