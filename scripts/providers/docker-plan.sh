#!/usr/bin/env bash
set -euo pipefail
COMPOSE_FILE="${COMPOSE_FILE:-deploy/docker/docker-compose.production-hardening.yml}"
APPLY="${APPLY:-0}"
APPROVAL_ID="${APPROVAL_ID:-}"
python3 - <<PY
import os
from zai_coder.real_provider_adapters.routes import route_docker_compose_plan
print(route_docker_compose_plan({"compose_file":"${COMPOSE_FILE}","apply":"${APPLY}"=="1","approval_id":"${APPROVAL_ID}","env":dict(os.environ),"scopes":["providers:plan","providers:apply"]}))
PY
