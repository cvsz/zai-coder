#!/usr/bin/env bash
set -euo pipefail
APPLY="${APPLY:-0}"
python3 - <<PY
from zai_coder.deployment_core.backup_restore import create_backup
print(create_backup(".", "backups", apply="${APPLY}"=="1").to_dict())
PY
