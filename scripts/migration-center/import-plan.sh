#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.data_import_export_migration_center.routes import route_import_plan
print(route_import_plan())
PY
