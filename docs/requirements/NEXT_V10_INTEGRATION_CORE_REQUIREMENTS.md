# ZAI Coder Control Plane v10 — Integration Core Requirements

## Added in v10

- Integration registry.
- GitHub integration plans.
- Cloudflare integration plans.
- Docker integration plans.
- Hugging Face publish/upload/Space scaffold plans.
- Social media draft adapters.
- Storage backend plans.
- Notification payload draft adapters.
- OpenAPI schema export.
- Integration route registry.
- Deployment server integration routes.

## Integration providers

```text
github
cloudflare
docker
huggingface
social
storage
notifications
openapi
```

## Safety

- All adapters are dry-run-first.
- No external mutation by default.
- No credential storage.
- No automatic social posting.
- No automatic Git push.
- No Cloudflare production mutation.
- No Docker volume deletion.
- No Hugging Face upload without explicit operator action.
- Exact-path Git publish only.
