#!/usr/bin/env bash
set -euo pipefail
QUERY="${QUERY:-release}"
python3 - <<PY
from zai_coder.agent_marketplace_and_skills.routes import route_marketplace_search
print(route_marketplace_search("${QUERY}"))
PY
