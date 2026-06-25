#!/usr/bin/env bash
set -euo pipefail
if [ "${APPLY:-0}" != "1" ]; then echo "DRY-RUN: set APPLY=1 to write migration evidence/report files."; exit 0; fi
python3 - <<'PY'
from zai_coder.data_import_export_migration_center.routes import route_migration_export
print(route_migration_export())
PY
