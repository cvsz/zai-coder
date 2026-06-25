#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.data_import_export_migration_center.routes import route_mapping_catalog
print(route_mapping_catalog())
PY
