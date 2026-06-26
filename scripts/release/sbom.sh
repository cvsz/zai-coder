#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.deployment_core.sbom import write_sbom
sbom = write_sbom(".", "release/SBOM.json")
print({"components": len(sbom["components"]), "path": "release/SBOM.json"})
PY
