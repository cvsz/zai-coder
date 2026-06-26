#!/usr/bin/env bash
set -euo pipefail
if [ "${APPLY:-0}" != "1" ]; then echo "DRY-RUN: set APPLY=1 to write scalability evidence/report files."; exit 0; fi
python3 - <<'PY'
from zai_coder.multi_region_edge_scalability_planner.routes import route_scalability_export
print(route_scalability_export())
PY
