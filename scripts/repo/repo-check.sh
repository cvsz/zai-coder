#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.github_ready_core.repo_check import repo_ready_report
report = repo_ready_report(".")
print(report)
if not report["ok"]:
    raise SystemExit(1)
PY
