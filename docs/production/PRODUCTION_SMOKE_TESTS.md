# Production Smoke Tests

## Generate plan

```bash
make production-smoke-plan
```

## Required checks

- `/healthz` returns 200
- `/readyz` returns 200
- `/openapi.json` returns 200
- protected API routes reject missing session
