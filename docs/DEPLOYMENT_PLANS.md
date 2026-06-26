# Deployment Plans

ZAI Coder supports a `deploy` command to generate production-ready templates and checklists without risking in-place execution logic against the local host.

## Supported Targets
- **SystemD**: Native bare-metal linux daemon processes targeting virtual environments.
- **Docker**: Containerized architecture shipping with `docker-compose.yml` configs.
- **NGINX**: Reverse proxy bindings restricting port traversals.

## Workflows

**Generate a Review Plan**
```bash
./zai-coder deploy plan --target systemd
./zai-coder deploy plan --target docker
```

**Render to Output Files**
Renders strictly ensure paths remain sandboxed inside the `./out/` workspace. Sudo operations are intentionally excluded; execution is entirely dependent on user operator delegation.

```bash
./zai-coder deploy render --target systemd --out out/deploy/systemd
```

## Security Profile
- Emits localhost bindings (e.g., `127.0.0.1:8765`) preventing naive 0.0.0.0 external exposure defaults (unless explicitly overriden in Docker boundaries where the mapping manages local binding).
- Never runs `systemctl`.
- Output rendering strictly path-checks against directory traversal attacks.
