#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.agent_marketplace_and_skills.routes import route_skill_catalog, route_agent_catalog
print(route_skill_catalog())
print(route_agent_catalog())
PY
