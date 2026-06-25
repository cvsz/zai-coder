#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.production_hardening_core.ops.backup_policy import default_backup_policy
policy = default_backup_policy()
print({"policy": policy.to_dict(), "issues": policy.validate()})
PY
