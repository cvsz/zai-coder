#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.team_collaboration_workspaces.routes import route_team_review_queue
print(route_team_review_queue())
PY
