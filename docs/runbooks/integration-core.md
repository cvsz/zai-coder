# Runbook — Integration Core

## Purpose

Generate safe plans for external integrations without automatically mutating external services.

## Demos

```bash
make integration-core
make github-integration-demo
make cloudflare-plan-demo
make docker-status-demo
make huggingface-plan-demo
make social-draft-demo
make storage-plan-demo
make notification-demo
make openapi-export
```

## Server routes

```text
/api/integrations
/api/integrations/github/status-plan
/api/integrations/docker/status-plan
/openapi.json
```

## Safety

- Review all commands before executing.
- Keep credentials in environment variables or secret managers.
- No automatic posting, uploading, pushing, deploying, or deleting.
