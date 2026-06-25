#!/usr/bin/env bash
set -euo pipefail

APPLY="${APPLY:-0}"
ARCHIVE="${ARCHIVE:-}"

if [ -z "$ARCHIVE" ]; then
  echo "ARCHIVE is required"
  exit 2
fi

python3 - <<PY
from zai_coder.deploy_installer_core.backup_restore import restore_plan
print(restore_plan("${ARCHIVE}"))
PY

if [ "$APPLY" != "1" ]; then
  echo "DRY-RUN: set APPLY=1 to restore after review."
  exit 0
fi

tar -tzf "$ARCHIVE" >/dev/null
tar -xzf "$ARCHIVE" -C .
make healthcheck
