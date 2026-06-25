#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.feedback_roadmap_center.routes import route_feedback_links
print(route_feedback_links())
PY
