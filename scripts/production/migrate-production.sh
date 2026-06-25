#!/usr/bin/env bash
set -euo pipefail
APPLY="${APPLY:-0}"
DB_PATH="${DB_PATH:-data/zai-prod.db}"
python3 - <<PY
from zai_coder.production_hardening_core.migrations.manager import RevisionManager
print(RevisionManager("${DB_PATH}").upgrade(apply="${APPLY}"=="1"))
PY
