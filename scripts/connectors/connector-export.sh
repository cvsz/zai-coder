#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.plugin_connector_hub.routes import route_connector_export, route_connector_import_validate
print(route_connector_export())
print(route_connector_import_validate())
PY
