#!/usr/bin/env bash
set -euo pipefail
if [ "${APPLY:-0}" != "1" ]; then echo "DRY-RUN: set APPLY=1 to write security evidence/report files."; exit 0; fi
python3 - <<'PY'
from zai_coder.security_operations_threat_monitoring.routes import route_security_evidence_export
print(route_security_evidence_export())
PY
