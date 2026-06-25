#!/usr/bin/env bash
set -euo pipefail
LOG_PATH="${LOG_PATH:-logs/zai-coder.log}"
LINES="${LINES:-100}"
python3 - <<PY
from zai_coder.operations_control_center.log_viewer import tail_log
print(tail_log("${LOG_PATH}", int("${LINES}")))
PY
