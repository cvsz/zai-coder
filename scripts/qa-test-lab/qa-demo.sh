#!/usr/bin/env bash
set -euo pipefail
if [ "${APPLY:-0}" != "1" ]; then echo "DRY-RUN: set APPLY=1 to write QA demo files."; exit 0; fi
python3 - <<'PY'
from zai_coder.quality_assurance_test_lab.routes import route_qa_demo
print(route_qa_demo())
PY
