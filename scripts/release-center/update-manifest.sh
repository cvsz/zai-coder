#!/usr/bin/env bash
set -euo pipefail
APPLY="${APPLY:-0}"
if [ "$APPLY" != "1" ]; then
  echo "DRY-RUN: set APPLY=1 to write demo update manifest."
  exit 0
fi
python3 - <<'PY'
from zai_coder.release_automation_update_center.routes import route_update_manifest_demo, route_update_manifest_schema
print(route_update_manifest_demo())
print(route_update_manifest_schema())
PY
