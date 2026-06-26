#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.multi_region_edge_scalability_planner.routes import route_scaling_scenarios
print(route_scaling_scenarios())
PY
