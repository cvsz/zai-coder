#!/usr/bin/env bash
set -euo pipefail
if [ "${APPLY:-0}" != "1" ]; then echo "DRY-RUN: set APPLY=1 to write DR evidence/report files."; exit 0; fi
python3 - <<'PY'
from zai_coder.backup_restore_disaster_recovery.routes import route_recovery_evidence
print(route_recovery_evidence())
PY
