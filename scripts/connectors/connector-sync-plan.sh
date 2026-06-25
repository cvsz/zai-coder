#!/usr/bin/env bash
set -euo pipefail
CONNECTOR_ID="${CONNECTOR_ID:-github}"
python3 - <<PY
from zai_coder.plugin_connector_hub.routes import route_connector_sync_plan, route_connector_sync_policy
print(route_connector_sync_plan("${CONNECTOR_ID}"))
print(route_connector_sync_policy())
PY
