#!/usr/bin/env bash
set -euo pipefail
APPLY="${APPLY:-0}"
if [ "$APPLY" != "1" ]; then
  echo "DRY-RUN: set APPLY=1 to install demo connector in local SQLite."
  exit 0
fi
python3 - <<'PY'
from zai_coder.plugin_connector_hub.routes import route_connector_install_demo
print(route_connector_install_demo())
PY
