# Real Provider Adapters Guide

Provider wrappers are execution-aware and dry-run-first.

```bash
make provider-env-check PROVIDER=github
make github-provider-plan REPO_NAME=zai-coder-control-plane
make cloudflare-provider-plan HOSTNAME=zai.zeaz.dev
make docker-provider-plan
make postgres-provider-plan
```

Apply requires `APPLY=1`, valid provider environment, approval id, permission, and audit log.
