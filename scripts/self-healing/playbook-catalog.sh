#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.self_healing_operations.routes import route_playbook_catalog
print(route_playbook_catalog())
PY
