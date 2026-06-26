#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.package_registry_marketplace_publishing.routes import route_package_catalog
print(route_package_catalog())
PY
