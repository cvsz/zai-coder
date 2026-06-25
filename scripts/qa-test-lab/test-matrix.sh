#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.quality_assurance_test_lab.routes import route_test_matrix
print(route_test_matrix())
PY
