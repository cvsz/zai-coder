#!/usr/bin/env bash
set -euo pipefail
QUERY="${QUERY:-billing charge}"
python3 - <<PY
from zai_coder.knowledge_base_help_center.routes import route_help_search
print(route_help_search("${QUERY}"))
PY
