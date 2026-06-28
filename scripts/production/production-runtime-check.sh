#!/usr/bin/env bash
# v51 Production Runtime Gate script
# Validates production dependencies, ASGI import, and health probes.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

echo "== v51 Production Runtime Gate =="
echo "root: ${ROOT}"

python3 - <<'PY'
import json, sys
from zai_coder.production_runtime.gate import run_runtime_gate
report = run_runtime_gate()
print(json.dumps(report, indent=2))
if not report["ok"]:
    sys.exit(1)
PY

echo ""
echo "v51 Production Runtime Gate: OK"
