# ZAI Coder Control Plane v13 — Production Hardening Requirements

## Added in v13

- FastAPI app factory and ASGI entrypoint.
- Real session auth foundation with hashed session tokens.
- Authorization helper for session-protected routes.
- PostgreSQL adapter and DSN validation.
- Alembic-style revision manager.
- JSON logging configuration.
- Backup policy model.
- Production smoke test plan.
- Hardened Dockerfile.
- Hardened Docker Compose profile.
- Hardened systemd service.
- Cloudflare Access deployment guide.
- Monitoring/logging docs.
- Backup policy docs.
- Production smoke test docs.

## Safety

- Runtime app binds to localhost by default.
- Session tokens are hashed at rest.
- Raw session token is returned only once.
- Public exposure should use Cloudflare Access.
- Database DSN is never printed with credentials.
- Docker profile uses non-root user and dropped capabilities.
