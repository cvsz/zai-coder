#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.multi_region_edge_scalability_planner.routes import route_region_readiness
print(route_region_readiness())
PY
