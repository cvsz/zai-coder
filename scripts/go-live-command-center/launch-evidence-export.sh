#!/usr/bin/env bash
set -euo pipefail
if [ "${APPLY:-0}" != "1" ]; then echo "DRY-RUN: set APPLY=1 to write launch evidence/report files."; exit 0; fi
python3 - <<'PY'
from zai_coder.production_readiness_go_live_command_center.routes import route_launch_evidence_export
print(route_launch_evidence_export())
PY
