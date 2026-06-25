#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.data_import_export_migration_center.routes import route_migration_status
print(route_migration_status())
PY
