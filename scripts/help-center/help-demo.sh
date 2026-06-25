#!/usr/bin/env bash
set -euo pipefail
APPLY="${APPLY:-0}"
if [ "$APPLY" != "1" ]; then
  echo "DRY-RUN: set APPLY=1 to write help center demo export/report files."
  exit 0
fi
python3 - <<'PY'
from zai_coder.knowledge_base_help_center.routes import route_help_demo
print(route_help_demo())
PY
