#!/usr/bin/env bash
set -euo pipefail
if [ "${APPLY:-0}" != "1" ]; then echo "DRY-RUN: set APPLY=1 to write demo files."; exit 0; fi
python3 - <<'PY'
from zai_coder.team_collaboration_workspaces.routes import route_team_demo
print(route_team_demo())
PY
