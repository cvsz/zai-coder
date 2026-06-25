# Recovery and Rollback

Failed operations generate a recovery plan.

Rollback hooks currently cover:

- Docker Compose deployment
- Cloudflare DNS route
- PostgreSQL migration

Use:

```bash
make execution-recovery-plan PROVIDER=docker ACTION=docker_compose_up
make execution-rollback-hooks
```
