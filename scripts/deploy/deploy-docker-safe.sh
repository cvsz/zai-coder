#!/usr/bin/env bash
set -euo pipefail

APPLY="${APPLY:-0}"
COMPOSE_FILE="${COMPOSE_FILE:-deploy/docker/docker-compose.production-hardening.yml}"

docker compose -f "$COMPOSE_FILE" config

if [ "$APPLY" != "1" ]; then
  echo "DRY-RUN: set APPLY=1 to build and start Docker Compose."
  exit 0
fi

docker compose -f "$COMPOSE_FILE" up --build -d
docker compose -f "$COMPOSE_FILE" ps
