# ZAI Coder v8 — Full App Studio Requirements

## Target

`zai-coder-control-plane-v8-app-studio.zip`

## Scope

Turn the control plane into a full local-first app studio.

## Add next

### UI

- Unified admin dashboard.
- Members UI.
- Billing UI.
- Creative project UI.
- Workspace UI.
- Agent run UI.
- Audit dashboard.
- Settings UI.

### Backend

- API auth integration.
- SQLite migrations manager.
- Local background worker.
- WebSocket run streaming.
- Event bus.
- Notification center.

### Monetization

- Billing dashboard.
- Quota dashboard.
- Usage charts.
- Reconciliation dashboard.
- Sandbox checkout UI.
- Provider adapter boundary.

### Deployment

- Dockerfile.
- docker-compose.yml.
- systemd service.
- Cloudflare tunnel checklist.
- GitHub release artifact workflow.

### Safety

- Dry-run-first still required.
- APPLY=1 for mutations.
- Secrets via env only.
- Audit every mutation.
