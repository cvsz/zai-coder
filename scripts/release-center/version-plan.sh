#!/usr/bin/env bash
set -euo pipefail
CURRENT="${CURRENT:-v28.0.0}"
BUMP="${BUMP:-minor}"
CHANNEL="${CHANNEL:-stable}"
python3 - <<PY
from zai_coder.release_automation_update_center.routes import route_version_plan
print(route_version_plan("${CURRENT}", "${BUMP}", "${CHANNEL}"))
PY
