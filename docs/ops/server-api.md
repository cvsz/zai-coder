# API Server Operations

ZAI Coder runs a local API server to communicate with the TUI, future UI clients, and IDE integrations.

## Core Endpoints

- `GET /health`: Returns `{"status": "ok"}`
- `GET /version`: Returns `{"version": "..."}` matching the current package version.
- `GET /agents`, `GET /skills`: Exposes current registry.

## Security Posture

- By default, the server binds **only** to `127.0.0.1` (localhost).
- Remote binding is blocked unless explicitly configured via `--host 0.0.0.0`.
- Authentication bypasses are strictly prohibited.
