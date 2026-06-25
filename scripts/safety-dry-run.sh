#!/usr/bin/env bash
set -euo pipefail

APPLY="${APPLY:-0}"
LABEL=""

usage() {
  cat <<'USAGE'
Usage: scripts/safety-dry-run.sh [--apply 0|1] [--label NAME] -- COMMAND [ARGS...]

Default is dry-run. The command is printed but not executed unless APPLY=1
or --apply 1 is provided. Dangerous git/shell patterns are blocked either way.
USAGE
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --apply)
      APPLY="${2:-0}"; shift 2 ;;
    --label)
      LABEL="${2:-}"; shift 2 ;;
    --help|-h)
      usage; exit 0 ;;
    --)
      shift; break ;;
    *)
      echo "Unknown option: $1" >&2
      usage >&2
      exit 2 ;;
  esac
done

if [[ $# -eq 0 ]]; then
  echo "No command provided" >&2
  usage >&2
  exit 2
fi

cmd_raw="$*"
cmd_display=""
for arg in "$@"; do
  printf -v quoted '%q' "$arg"
  cmd_display+="${quoted} "
done
cmd_display="${cmd_display% }"
# Use raw command for policy matching so wrapped commands like
# ./zai-coder run "git add ." are still blocked before execution.
cmd_lower="$(printf '%s' "$cmd_raw" | tr '[:upper:]' '[:lower:]')"

block() {
  echo "SAFETY BLOCKED: $1" >&2
  echo "Command: $cmd_display" >&2
  exit 126
}

[[ "$cmd_lower" =~ (^|[[:space:]])git[[:space:]]+add[[:space:]]+\.($|[[:space:]]) ]] && block "use exact-path staging, not git add ."
[[ "$cmd_lower" =~ (^|[[:space:]])git[[:space:]]+add[[:space:]]+-a($|[[:space:]]) ]] && block "use exact-path staging, not git add -A"
[[ "$cmd_lower" =~ (^|[[:space:]])git[[:space:]]+add[[:space:]]+--all($|[[:space:]]) ]] && block "use exact-path staging, not git add --all"
[[ "$cmd_lower" =~ --no-verify ]] && block "--no-verify bypasses checks"
[[ "$cmd_lower" =~ (^|[[:space:]])git[[:space:]]+push.*(--force|-f|--force-with-lease) ]] && block "force push is disabled"
[[ "$cmd_lower" =~ (^|[[:space:]])sudo[[:space:]]+rm[[:space:]]+-rf ]] && block "sudo rm -rf requires manual review"
[[ "$cmd_lower" =~ (^|[[:space:]])rm[[:space:]]+-rf[[:space:]]+(/|~|\.|\$home)($|[[:space:]]) ]] && block "broad rm -rf is dangerous"
[[ "$cmd_lower" =~ chmod[[:space:]]+-r[[:space:]]+777 ]] && block "recursive chmod 777 is unsafe"
[[ "$cmd_lower" =~ (curl|wget).*\|[[:space:]]*(sudo[[:space:]]+)?(bash|sh) ]] && block "pipe-to-shell requires manual review"
[[ "$cmd_lower" =~ apps/zlms/ ]] && block "apps/zlms/** is protected by default"
[[ "$cmd_lower" =~ (^|[[:space:]])\.env($|[[:space:]]) ]] && block ".env files are protected"
[[ "$cmd_lower" =~ (node_modules/|/node_modules|dist/|\.next/|coverage/|reports/|vendor/ai-assets/) ]] && block "generated artifact path is protected"

prefix="[DRY-RUN]"
[[ -n "$LABEL" ]] && prefix="[DRY-RUN:$LABEL]"

if [[ "$APPLY" != "1" ]]; then
  echo "$prefix $cmd_display"
  echo "Set APPLY=1 to execute."
  exit 0
fi

echo "[APPLY] $cmd_display"
exec "$@"
