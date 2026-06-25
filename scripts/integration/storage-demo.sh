#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
from zai_coder.integration_core.adapters.storage_backends import local_storage_plan, object_storage_upload_plan, StorageConfig
print(local_storage_plan("storage").to_dict())
print(object_storage_upload_plan(StorageConfig("r2", bucket="zai-artifacts", endpoint_url="https://example.r2.cloudflarestorage.com"), "release/a.zip", "a.zip").to_dict())
PY
