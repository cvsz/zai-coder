#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.feedback_roadmap_center.routes import route_roadmap_customer_view
print(route_roadmap_customer_view())
PY
