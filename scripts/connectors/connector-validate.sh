#!/usr/bin/env bash
set -euo pipefail
CONNECTOR_ID="${CONNECTOR_ID:-github}"
python3 - <<PY
from zai_coder.plugin_connector_hub.routes import route_connector_validate_demo, route_connector_security_report
print(route_connector_validate_demo())
print(route_connector_security_report("${CONNECTOR_ID}"))
PY
