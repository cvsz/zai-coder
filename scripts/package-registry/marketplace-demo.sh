#!/usr/bin/env bash
set -euo pipefail
if [ "${APPLY:-0}" != "1" ]; then echo "DRY-RUN: set APPLY=1 to write marketplace demo files."; exit 0; fi
python3 - <<'PY'
from zai_coder.package_registry_marketplace_publishing.routes import route_marketplace_demo
print(route_marketplace_demo())
PY
