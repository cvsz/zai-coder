#!/usr/bin/env bash
set -euo pipefail
if [ "${APPLY:-0}" != "1" ]; then echo "DRY-RUN: set APPLY=1 to write final release demo files."; exit 0; fi
python3 - <<'PY'
from zai_coder.final_enterprise_release_pack.routes import route_final_release_demo
print(route_final_release_demo())
PY
