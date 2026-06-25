#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.real_provider_adapters.routes import route_providers_status, route_provider_actions
print(route_providers_status())
print(route_provider_actions())
PY
