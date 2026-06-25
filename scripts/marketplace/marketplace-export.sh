#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.agent_marketplace_and_skills.routes import route_marketplace_export, route_marketplace_import_validate
print(route_marketplace_export())
print(route_marketplace_import_validate())
PY
