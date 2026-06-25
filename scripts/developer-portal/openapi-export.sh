#!/usr/bin/env bash
set -euo pipefail
if [ "${APPLY:-0}" != "1" ]; then echo "DRY-RUN: set APPLY=1 to write OpenAPI export."; exit 0; fi
python3 - <<'PY'
from zai_coder.developer_portal_api_docs.routes import route_openapi_export
print(route_openapi_export()["path"])
PY
