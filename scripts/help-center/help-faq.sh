#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.knowledge_base_help_center.routes import route_help_faq
print(route_help_faq())
PY
