#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.integration_core.adapters.social_drafts import create_social_drafts
print(create_social_drafts("ZAI Coder v10", "Integration Core is ready with dry-run-first adapters.").to_dict())
PY
