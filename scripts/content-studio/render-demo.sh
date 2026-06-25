#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.template_content_studio.routes import route_render_demo
print(route_render_demo())
PY
