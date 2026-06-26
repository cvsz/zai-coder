#!/usr/bin/env bash
set -euo pipefail
APPLY="${APPLY:-0}"
if [ "$APPLY" != "1" ]; then
  echo "DRY-RUN: set APPLY=1 to enable demo connector in local SQLite."
  exit 0
fi
python3 - <<'PY'
from zai_coder.plugin_connector_hub.routes import route_connector_enable_demo
print(route_connector_enable_demo())
PY
