#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.feedback_roadmap_center.routes import route_changelog_feedback_loop
print(route_changelog_feedback_loop())
PY
