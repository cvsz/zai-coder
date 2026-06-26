#!/usr/bin/env bash
set -euo pipefail
OUT="${OUT:-assets/gateway/gateway-openapi.json}"
mkdir -p "$(dirname "$OUT")"
python3 - <<PY
from pathlib import Path
import json
from zai_coder.production_api_gateway.routes import route_gateway_openapi
Path("${OUT}").write_text(json.dumps(route_gateway_openapi(), indent=2, sort_keys=True), encoding="utf-8")
print("${OUT}")
PY
