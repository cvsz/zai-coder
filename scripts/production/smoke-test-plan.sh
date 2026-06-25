#!/usr/bin/env bash
set -euo pipefail
BASE_URL="${BASE_URL:-http://127.0.0.1:8765}"
python3 - <<PY
from zai_coder.production_hardening_core.ops.smoke_tests import production_smoke_test_plan
print(production_smoke_test_plan("${BASE_URL}"))
PY
