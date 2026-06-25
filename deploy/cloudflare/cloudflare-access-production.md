# Cloudflare Access Deployment Guide

## Goal

Expose ZAI Coder through Cloudflare Tunnel only after auth/session hardening is enabled.

## Required controls

- Cloudflare Access application in front of the hostname.
- Local app binds to `127.0.0.1:8765`.
- Tunnel service points to `http://127.0.0.1:8765`.
- `/api/status` requires session header.
- Provider credentials stay outside the repo.

## Example hostname

```text
zai.zeaz.dev
```

## Tunnel ingress

```yaml
ingress:
  - hostname: zai.zeaz.dev
    service: http://127.0.0.1:8765
  - service: http_status:404
```

## Validation

```bash
make production-smoke-plan
curl http://127.0.0.1:8765/healthz
curl http://127.0.0.1:8765/readyz
```
