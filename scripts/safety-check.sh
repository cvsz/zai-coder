#!/usr/bin/env bash
set -euo pipefail

ROOT="${1:-.}"
STRICT="${STRICT:-0}"
fail=0
warn=0

cd "$ROOT"

echo "== ZAI Coder safety check =="
echo "root: $(pwd)"

check_secret_pattern() {
  local label="$1"
  local pattern="$2"
  local hits
  hits=$(grep -RInE --exclude-dir=.git --exclude-dir=.venv --exclude-dir=__pycache__ --exclude-dir=node_modules --exclude-dir=dist --exclude-dir=.pytest_cache --exclude='*.pyc' "$pattern" . 2>/dev/null || true)
  if [[ -n "$hits" ]]; then
    echo ""
    echo "SECRET CHECK FAILED: $label"
    printf '%s\n' "$hits" | head -20
    fail=1
  fi
}

check_secret_pattern "OpenRouter key" 'sk-or-v1-[A-Za-z0-9_-]+'
check_secret_pattern "OpenAI-style key" 'sk-[A-Za-z0-9]{20,}'
check_secret_pattern "AWS access key" 'AKIA[0-9A-Z]{16}'
check_secret_pattern "private key block" 'BEGIN (RSA |OPENSSH |EC |DSA )?PRIVATE KEY'

echo ""
echo "== Generated/noisy artifact warnings =="
while IFS= read -r p; do
  [[ -z "$p" ]] && continue
  echo "WARN generated/noisy path: $p"
  warn=1
done < <(find . \
  -path './.git' -prune -o \
  \( -path './node_modules' -o -path './dist' -o -path './.next' -o -path './coverage' -o -path './reports' -o -path './.pytest_cache' -o -path './out' \) \
  -print 2>/dev/null)

if [[ "$STRICT" == "1" && "$warn" == "1" ]]; then
  fail=1
fi

if [[ "$fail" == "1" ]]; then
  echo ""
  echo "Safety check: FAILED"
  exit 1
fi

echo ""
echo "Safety check: OK"
exit 0
