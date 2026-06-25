# ZAI Coder Control Plane v8 — App Studio Requirements

## Added in v8

- Unified web admin dashboard renderer.
- API key manager with salted hashes.
- SQLite migrations manager.
- Local background worker queue.
- Streaming event buffer.
- Framework-neutral route registry.
- Dockerfile.
- docker-compose.yml.
- systemd service template.
- Cloudflare Tunnel checklist.
- deploy scripts.
- v9 deployment requirements.

## Safety

- Bind locally first.
- No public exposure without auth.
- Raw API keys returned only at creation time.
- Database migrations are dry-run-first.
- Deploy scripts require `APPLY=1`.
- No secrets committed.
