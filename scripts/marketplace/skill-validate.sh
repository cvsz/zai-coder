#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.agent_marketplace_and_skills.routes import route_skill_validate_demo, route_skill_security_report
print(route_skill_validate_demo())
print(route_skill_security_report())
PY
