#!/usr/bin/env bash
set -euo pipefail
OUT="${OUT:-docs/integrations/openapi.json}"
mkdir -p "$(dirname "$OUT")"
python3 - <<PY
from pathlib import Path
from zai_coder.integration_core.openapi import export_openapi_json
Path("${OUT}").write_text(export_openapi_json(), encoding="utf-8")
print("${OUT}")
PY
