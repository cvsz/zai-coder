#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.real_provider_adapters.routes import route_provider_audit
print(route_provider_audit())
PY
