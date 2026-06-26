#!/usr/bin/env bash
set -euo pipefail
APPLY="${APPLY:-0}"
if [ "$APPLY" != "1" ]; then
  echo "DRY-RUN: set APPLY=1 to write demo evidence inventory."
  exit 0
fi
python3 - <<'PY'
from zai_coder.enterprise_compliance_center.routes import route_evidence_demo
print(route_evidence_demo())
PY
