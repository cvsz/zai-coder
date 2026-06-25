#!/usr/bin/env bash
set -euo pipefail
APPLY="${APPLY:-0}"
if [ "$APPLY" != "1" ]; then
  echo "DRY-RUN: set APPLY=1 to write admin export and audit demo."
  exit 0
fi
python3 - <<'PY'
from zai_coder.enterprise_admin_console.routes import route_admin_action_demo
print(route_admin_action_demo())
PY
