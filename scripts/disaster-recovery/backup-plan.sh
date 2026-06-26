#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.backup_restore_disaster_recovery.routes import route_backup_plan
print(route_backup_plan())
PY
