#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.feedback_roadmap_center.routes import route_release_link_plan
print(route_release_link_plan())
PY
