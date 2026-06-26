#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.deploy_installer_core.go_live import go_live_checklist
for item in go_live_checklist():
    print(f"[{'REQUIRED' if item['required'] else 'OPTIONAL'}] {item['area']}: {item['item']}")
PY
