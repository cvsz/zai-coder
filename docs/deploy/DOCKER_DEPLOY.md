# Docker Deploy Guide

## Dry-run/check

```bash
make docker-build-plan
```

## Build

```bash
make docker-build APPLY=1
```

## Compose test

```bash
docker compose config
docker compose up --build
```

## Safety

- Bind to `127.0.0.1` by default.
- Do not mount secret directories.
- Do not publish without API auth.
