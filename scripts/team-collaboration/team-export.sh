#!/usr/bin/env bash
set -euo pipefail
if [ "${APPLY:-0}" != "1" ]; then echo "DRY-RUN: set APPLY=1 to write team export files."; exit 0; fi
python3 - <<'PY'
from zai_coder.team_collaboration_workspaces.routes import route_team_export
print(route_team_export())
PY
