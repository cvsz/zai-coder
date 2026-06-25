# Go-Live Checklist

```bash
make go-live-checklist
```

## Required

- Tests pass.
- Repo check passes.
- Secret scan passes.
- `.env` exists and is not committed.
- Backup created.
- Migrations applied.
- Service starts on localhost.
- `/healthz` and `/readyz` pass.
- Cloudflare Access enabled.
- Restore test complete.
- Release checksums and SBOM generated.
