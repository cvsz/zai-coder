#!/usr/bin/env bash
set -euo pipefail
OUT="${OUT:-docs/final/openapi.full.json}"
mkdir -p "$(dirname "$OUT")"
python3 - <<PY
from pathlib import Path
from zai_coder.app_studio_final.openapi_full import export_full_openapi_json
Path("${OUT}").write_text(export_full_openapi_json(), encoding="utf-8")
print("${OUT}")
PY
