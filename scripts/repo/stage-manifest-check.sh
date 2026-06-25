#!/usr/bin/env bash
set -euo pipefail
MANIFEST="${MANIFEST:-docs/github/STAGE_MANIFEST.v12-github-ready.txt}"
python3 - <<PY
from zai_coder.github_ready_core.stage_manifest import load_stage_manifest, validate_stage_manifest
result = validate_stage_manifest(load_stage_manifest("${MANIFEST}"))
print(result)
if not result["ok"]:
    raise SystemExit(1)
PY
