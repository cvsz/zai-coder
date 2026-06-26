#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.quality_assurance_test_lab.routes import route_qa_status
print(route_qa_status())
PY
