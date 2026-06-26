#!/usr/bin/env bash
set -euo pipefail
APPLY="${APPLY:-0}"
if [ "$APPLY" != "1" ]; then
  echo "DRY-RUN: set APPLY=1 to create tenant-scoped API key."
  exit 0
fi
python3 - <<'PY'
from zai_coder.multi_tenant_control.routes import route_create_tenant_api_key
print(route_create_tenant_api_key())
PY
