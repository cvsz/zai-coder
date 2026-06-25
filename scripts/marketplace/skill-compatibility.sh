#!/usr/bin/env bash
set -euo pipefail
AGENT_TYPE="${AGENT_TYPE:-builder}"
SKILL_ID="${SKILL_ID:-repo-planner}"
python3 - <<PY
from zai_coder.agent_marketplace_and_skills.routes import route_skill_compatibility
print(route_skill_compatibility("${AGENT_TYPE}", "${SKILL_ID}"))
PY
