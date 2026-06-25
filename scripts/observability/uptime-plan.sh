#!/usr/bin/env bash
set -euo pipefail
BASE_URL="${BASE_URL:-http://127.0.0.1:8765}"
PUBLIC_URL="${PUBLIC_URL:-https://zai.example.com}"
python3 - <<PY
from zai_coder.observability_suite.routes import route_uptime_plan
print(route_uptime_plan("${BASE_URL}", "${PUBLIC_URL}"))
PY
