#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.template_content_studio.routes import route_content_approval
print(route_content_approval())
PY
