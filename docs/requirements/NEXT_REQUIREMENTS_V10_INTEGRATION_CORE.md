# ZAI Coder v10 — Integration Core Requirements

## Target

`zai-coder-control-plane-v10-integration-core.zip`

## Scope

Real external integrations with dry-run-first adapter boundaries.

## Add next

- GitHub app/CLI integration routes.
- Cloudflare deploy adapter.
- Docker deployment adapter.
- Hugging Face dataset/model/Space upload plan.
- Social draft adapters:
  - X
  - LinkedIn
  - Facebook
  - Instagram
  - TikTok
  - YouTube
- Storage backends:
  - local filesystem
  - S3/R2-compatible object storage
- Notification adapters:
  - email
  - Slack
  - Discord
  - Telegram
- API auth middleware wired into server.
- Real FastAPI/Starlette option.
- OpenAPI schema export.

## Safety

- No external mutation without `APPLY=1`.
- No credentials in repository.
- Dry-run plans first.
- Audit every external action.
