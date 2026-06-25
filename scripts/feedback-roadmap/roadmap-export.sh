#!/usr/bin/env bash
set -euo pipefail
APPLY="${APPLY:-0}"
if [ "$APPLY" != "1" ]; then
  echo "DRY-RUN: set APPLY=1 to write customer roadmap export."
  exit 0
fi
python3 - <<'PY'
from zai_coder.feedback_roadmap_center.routes import route_roadmap_export
print(route_roadmap_export()["path"])
PY
