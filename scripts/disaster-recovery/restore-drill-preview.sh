#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.backup_restore_disaster_recovery.routes import route_restore_drill_preview
print(route_restore_drill_preview())
PY
