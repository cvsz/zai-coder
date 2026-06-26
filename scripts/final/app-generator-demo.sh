#!/usr/bin/env bash
set -euo pipefail
APP_NAME="${APP_NAME:-ZAI Demo App}"
APP_TYPE="${APP_TYPE:-web}"
python3 - <<PY
from zai_coder.app_studio_final.wizards.app_generator import generate_app_plan
print(generate_app_plan("${APP_NAME}", "${APP_TYPE}").to_dict())
PY
