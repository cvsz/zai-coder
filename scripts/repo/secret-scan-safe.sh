#!/usr/bin/env bash
set -euo pipefail

python3 - <<'PY'
from zai_coder.github_ready_core.secret_scan import scan_repo
report = scan_repo(".")
print(report)
if not report["ok"]:
    raise SystemExit(1)
PY

# Call existing safety-check.sh
STRICT="${STRICT:-0}"
export STRICT
bash ./scripts/safety-check.sh .
