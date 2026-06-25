#!/usr/bin/env bash
set -euo pipefail
APPLY="${APPLY:-0}"
DB_PATH="${DB_PATH:-data/zai-app.db}"
python3 - <<PY
from zai_coder.production_saas_core.cli.migrations_cli import migrations_command
print(migrations_command("${DB_PATH}", apply="${APPLY}"=="1"))
PY
