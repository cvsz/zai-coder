#!/usr/bin/env bash
set -euo pipefail

fail=0

echo "== CI pytest setup guard =="

shopt -s nullglob
workflow_files=(.github/workflows/*.yml .github/workflows/*.yaml)

for file in "${workflow_files[@]}"; do
  if grep -Eq 'python -m pytest|pytest -q|pytest ' "$file"; then
    if ! grep -Eq 'pip install.*pytest|python -m pip install.*pytest|pip install -e|python -m pip install -e|uv pip install|poetry install|hatch|tox' "$file"; then
      echo "Workflow runs pytest without an obvious dependency install step: $file"
      fail=1
    else
      echo "ok $file"
    fi
  fi
done

if [ "$fail" -ne 0 ]; then
  echo "CI pytest dependency setup guard failed."
  exit 1
fi

echo "CI pytest setup guard passed"
