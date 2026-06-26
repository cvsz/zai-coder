#!/usr/bin/env bash
set -euo pipefail
COMMAND="${COMMAND:-echo hello}"
python3 - <<PY
from zai_coder.execution_runner.safety import command_safety_report
print(command_safety_report(tuple("${COMMAND}".split()), "."))
PY
