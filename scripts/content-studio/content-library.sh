#!/usr/bin/env bash
set -euo pipefail
APPLY="${APPLY:-0}"
if [ "$APPLY" != "1" ]; then
  echo "DRY-RUN: set APPLY=1 to write content library export."
  exit 0
fi
python3 - <<'PY'
from zai_coder.template_content_studio.routes import route_content_library
print(route_content_library()["path"])
PY
