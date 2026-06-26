#!/usr/bin/env bash
set -euo pipefail
if [ "${APPLY:-0}" != "1" ]; then echo "DRY-RUN: set APPLY=1 to write developer portal demo files."; exit 0; fi
python3 - <<'PY'
from zai_coder.developer_portal_api_docs.routes import route_developer_demo
print(route_developer_demo())
PY
