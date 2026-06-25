#!/usr/bin/env bash
set -euo pipefail
APPLY="${APPLY:-0}"
ADMIN_EMAIL="${ADMIN_EMAIL:-admin@example.com}"
DB_PATH="${DB_PATH:-data/zai-app.db}"
python3 - <<PY
from zai_coder.deployment_core.admin_bootstrap import bootstrap_admin
print(bootstrap_admin("${DB_PATH}", "${ADMIN_EMAIL}", apply="${APPLY}"=="1").to_dict())
PY
