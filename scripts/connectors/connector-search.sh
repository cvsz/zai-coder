#!/usr/bin/env bash
set -euo pipefail
QUERY="${QUERY:-cloud}"
python3 - <<PY
from zai_coder.plugin_connector_hub.routes import route_connector_search
print(route_connector_search("${QUERY}"))
PY
