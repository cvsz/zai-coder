#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.agent_marketplace_and_skills.routes import route_marketplace_audit
print(route_marketplace_audit())
PY
