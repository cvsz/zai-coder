#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.integration_core.adapters.github_adapter import repo_status_plan, exact_path_publish_plan
print(repo_status_plan().to_dict())
print(exact_path_publish_plan(["README.md", "docs/requirements/FULL_PROJECT_REQUIREMENTS.md", "apps/zlms/blocked.md"]).to_dict())
PY
