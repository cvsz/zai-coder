#!/usr/bin/env bash
set -euo pipefail
SKILL_ID="${SKILL_ID:-repo-planner}"
AGENT_TYPE="${AGENT_TYPE:-builder}"
python3 - <<PY
from zai_coder.agent_marketplace_and_skills.routes import route_skill_install_policy, route_skill_enable_policy
print(route_skill_install_policy("${SKILL_ID}", "${AGENT_TYPE}"))
print(route_skill_enable_policy("${SKILL_ID}"))
PY
