#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.integration_core.adapters.huggingface_adapter import model_publish_plan, space_scaffold_plan
print(model_publish_plan("cvsz/zai-coder-demo").to_dict())
print(space_scaffold_plan("cvsz/zai-coder-space").to_dict())
PY
