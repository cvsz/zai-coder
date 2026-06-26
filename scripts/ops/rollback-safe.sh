#!/usr/bin/env bash
set -euo pipefail
VERSION="${VERSION:-previous}"
python3 - <<PY
from zai_coder.deploy_installer_core.upgrade_rollback import rollback_plan
print(rollback_plan("${VERSION}"))
PY
