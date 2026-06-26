#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.app_studio_final.workflow_builder import default_release_workflow
print(default_release_workflow().to_dict())
PY
