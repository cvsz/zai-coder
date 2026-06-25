#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.release_automation_update_center.routes import route_rollback_migration_demo
print(route_rollback_migration_demo())
PY
