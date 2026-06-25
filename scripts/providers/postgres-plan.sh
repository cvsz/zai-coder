#!/usr/bin/env bash
set -euo pipefail
DATABASE_URL="${DATABASE_URL:-postgresql://zai@127.0.0.1:5432/zai}"
APPLY="${APPLY:-0}"
APPROVAL_ID="${APPROVAL_ID:-}"
python3 - <<PY
import os
from zai_coder.real_provider_adapters.routes import route_postgres_migration_plan
print(route_postgres_migration_plan({"dsn":"${DATABASE_URL}","apply":"${APPLY}"=="1","approval_id":"${APPROVAL_ID}","env":dict(os.environ),"scopes":["providers:plan","providers:apply"]}))
PY
