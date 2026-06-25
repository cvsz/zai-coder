#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.production_api_gateway.routes import route_gateway_headers
print(route_gateway_headers())
PY
