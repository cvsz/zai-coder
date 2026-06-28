#!/usr/bin/env bash
set -euo pipefail

APPLY="${APPLY:-0}"
python3 - <<'PY'
from zai_coder.deploy_installer_core.backup_restore import backup_plan
print(backup_plan())
PY

if [ "$APPLY" != "1" ]; then
  echo "DRY-RUN: set APPLY=1 to create archive."
  exit 0
fi

mkdir -p backups
BACKUP_ITEMS=()
for item in data logs storage; do
  if [ -d "$item" ]; then
    BACKUP_ITEMS+=("$item")
  fi
done
tar --exclude=release --exclude=node_modules --exclude=.git --exclude=apps/zlms -czf "backups/zai-coder-control-plane-backup-$(date +%Y%m%d-%H%M%S).tar.gz" "${BACKUP_ITEMS[@]}"
