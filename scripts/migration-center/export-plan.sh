#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.data_import_export_migration_center.routes import route_export_plan
print(route_export_plan())
PY
