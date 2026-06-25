#!/usr/bin/env bash
set -euo pipefail
APPLY="${APPLY:-0}"
if [ "$APPLY" != "1" ]; then
  echo "DRY-RUN: set APPLY=1 to write roadmap report/export files."
  exit 0
fi
python3 - <<'PY'
from zai_coder.feedback_roadmap_center.routes import route_roadmap_report_demo
print(route_roadmap_report_demo())
PY
