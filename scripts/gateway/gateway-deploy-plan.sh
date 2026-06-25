#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.production_api_gateway.routes import route_gateway_deploy_plan, route_gateway_smoke_plan
print(route_gateway_deploy_plan())
print(route_gateway_smoke_plan())
PY
