#!/usr/bin/env bash
set -euo pipefail
CONNECTOR_ID="${CONNECTOR_ID:-github}"
python3 - <<PY
from zai_coder.plugin_connector_hub.routes import route_connector_env_check
print(route_connector_env_check("${CONNECTOR_ID}"))
PY
