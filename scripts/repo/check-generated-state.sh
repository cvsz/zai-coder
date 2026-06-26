#!/usr/bin/env bash
set -euo pipefail

fail=0

tracked_patterns=(
  'data/*.db'
  'data/**/*.db'
  '*.sqlite'
  '*.sqlite3'
  '**/*.sqlite'
  '**/*.sqlite3'
  'evidence/**/*.json'
  'identity/evidence/**/*.json'
  'marketplace/exports/**/*.json'
  'migration/exports/**/*.json'
  'security/evidence/**/*.json'
)

echo "== generated-state guard =="

for pattern in "${tracked_patterns[@]}"; do
  if git ls-files "$pattern" 2>/dev/null | grep -q .; then
    echo "Tracked generated-state candidates found for pattern: $pattern"
    git ls-files "$pattern"
    fail=1
  fi
done

if [ "$fail" -ne 0 ]; then
  echo "Generated runtime/evidence state is tracked. Move fixtures to tests/fixtures or docs, or untrack generated outputs with git rm --cached exact paths."
  exit 1
fi

echo "generated-state guard passed"
