#!/usr/bin/env bash
set -euo pipefail
DATABASE_URL="${DATABASE_URL:-postgresql://zai@127.0.0.1:5432/zai}"
python3 - <<PY
from zai_coder.production_hardening_core.db.postgres_adapter import PostgresSettings
settings = PostgresSettings("${DATABASE_URL}")
print({"issues": settings.validate(), "safe": settings.safe_dict()})
PY
