#!/usr/bin/env bash
set -euo pipefail
DB_PATH="${DB_PATH:-data/zai-worker.db}"
python3 - <<PY
from zai_coder.production_saas_core.cli.worker_daemon import worker_run_once
print(worker_run_once("${DB_PATH}"))
PY
