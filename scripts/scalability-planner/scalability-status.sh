#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.multi_region_edge_scalability_planner.routes import route_scalability_status
print(route_scalability_status())
PY
