#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.security_operations_threat_monitoring.routes import route_security_ops_status
print(route_security_ops_status())
PY
