#!/usr/bin/env bash
set -euo pipefail
APPLY="${APPLY:-0}"
if [ "$APPLY" != "1" ]; then
  echo "DRY-RUN: set APPLY=1 to create demo tenant in local SQLite store."
  exit 0
fi
python3 - <<'PY'
from zai_coder.multi_tenant_control.routes import route_create_tenant_demo
print(route_create_tenant_demo())
PY
