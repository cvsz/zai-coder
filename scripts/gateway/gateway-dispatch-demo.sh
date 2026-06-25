#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.production_api_gateway.routes import route_gateway_dispatch_demo, route_gateway_protected_demo
print(route_gateway_dispatch_demo())
print(route_gateway_protected_demo())
PY
