#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.template_content_studio.routes import route_template_variables
print(route_template_variables())
PY
