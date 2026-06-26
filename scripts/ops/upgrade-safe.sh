#!/usr/bin/env bash
set -euo pipefail
VERSION="${VERSION:-v0.14.0}"
python3 - <<PY
from zai_coder.deploy_installer_core.upgrade_rollback import upgrade_plan
print(upgrade_plan("${VERSION}"))
PY
