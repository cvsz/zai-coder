#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.security_operations_threat_monitoring.routes import route_threat_signals
print(route_threat_signals())
PY
