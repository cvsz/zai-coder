#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.package_registry_marketplace_publishing.routes import route_marketplace_status
print(route_marketplace_status())
PY
