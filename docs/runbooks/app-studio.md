# Runbook — ZAI App Studio

## Purpose

Operate the unified App Studio dashboard and local control plane.

## Preflight

```bash
python3 -m pytest -q
make app-studio
make app-dashboard-demo
make api-key-demo
make migration-plan
```

## API auth flow

1. Create API key.
2. Copy raw key once.
3. Store only in secret manager or local environment.
4. Verify requests.
5. Revoke if leaked.

## Deployment flow

1. Run tests.
2. Run safety scan.
3. Build Docker image dry-run.
4. Install systemd dry-run.
5. Configure Cloudflare Access.
6. Bind to localhost.
7. Expose via tunnel only after auth.

## Safety

- Never expose unauthenticated dashboard publicly.
- Never commit generated API keys.
- Never put provider secrets in repo.
