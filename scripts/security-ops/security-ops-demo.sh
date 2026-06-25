#!/usr/bin/env bash
set -euo pipefail
if [ "${APPLY:-0}" != "1" ]; then echo "DRY-RUN: set APPLY=1 to write security ops demo files."; exit 0; fi
python3 - <<'PY'
from zai_coder.security_operations_threat_monitoring.routes import route_security_ops_demo
print(route_security_ops_demo())
PY
