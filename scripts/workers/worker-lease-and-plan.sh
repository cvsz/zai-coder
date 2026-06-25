#!/usr/bin/env bash
set -euo pipefail
APPLY="${APPLY:-0}"
if [ "$APPLY" != "1" ]; then
  echo "DRY-RUN: set APPLY=1 to create/lease a local demo job and generate bridge plan."
  exit 0
fi
python3 - <<'PY'
from zai_coder.worker_orchestration.routes import route_worker_lease_and_plan
print(route_worker_lease_and_plan())
PY
