#!/usr/bin/env bash
set -euo pipefail
APPLY="${APPLY:-0}"
if [ "$APPLY" != "1" ]; then
  echo "DRY-RUN: set APPLY=1 to write rendered content demo/export files."
  exit 0
fi
python3 - <<'PY'
from zai_coder.template_content_studio.routes import route_content_demo
print(route_content_demo())
PY
