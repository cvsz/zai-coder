#!/usr/bin/env bash
set -euo pipefail
if [ "${APPLY:-0}" != "1" ]; then echo "DRY-RUN: set APPLY=1 to write identity evidence/report files."; exit 0; fi
python3 - <<'PY'
from zai_coder.enterprise_sso_identity_center.routes import route_identity_evidence_export
print(route_identity_evidence_export())
PY
