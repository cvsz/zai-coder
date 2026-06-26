#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.plugin_connector_hub.routes import route_connector_catalog
print(route_connector_catalog())
PY
