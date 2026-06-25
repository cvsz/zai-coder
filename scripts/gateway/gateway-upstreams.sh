#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.production_api_gateway.routes import route_gateway_upstreams
print(route_gateway_upstreams())
PY
