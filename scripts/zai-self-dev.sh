#!/usr/bin/env bash
set -Eeuo pipefail

CONFIG_FILE="${ZAI_SELF_DEV_CONFIG:-configs/zai-self-dev.env}"
REPO_DIR_DEFAULT="/home/zeazdev/zai-coder"

log() { printf '==> %s\n' "$*"; }
warn() { printf 'WARN: %s\n' "$*" >&2; }
die() { printf 'ERROR: %s\n' "$*" >&2; exit 1; }

load_config() {
  local repo_dir="${ZAI_REPO_DIR:-$REPO_DIR_DEFAULT}"

  if [[ -f "$repo_dir/$CONFIG_FILE" ]]; then
    # shellcheck disable=SC1090
    source "$repo_dir/$CONFIG_FILE"
  elif [[ -f "$repo_dir/configs/zai-self-dev.env.example" ]]; then
    # shellcheck disable=SC1090
    source "$repo_dir/configs/zai-self-dev.env.example"
  elif [[ -f "$CONFIG_FILE" ]]; then
    # shellcheck disable=SC1090
    source "$CONFIG_FILE"
  else
    warn "Config not found; using built-in defaults"
  fi

  ZAI_REPO_DIR="${ZAI_REPO_DIR:-$repo_dir}"
  ZAI_REPO_FULL_NAME="${ZAI_REPO_FULL_NAME:-cvsz/zai-coder}"
  ZAI_MAIN_BRANCH="${ZAI_MAIN_BRANCH:-main}"
  ZAI_VENV="${ZAI_VENV:-/home/zeazdev/.venvs/zai-coder}"
  ZAI_MASTER_PROMPT="${ZAI_MASTER_PROMPT:-docs/prompts/MASTER-FINAL-IMPLEMENTATION.md}"
  ZAI_PHASE_PROMPT="${ZAI_PHASE_PROMPT:-docs/prompts/25-self-queue-production.md}"
  ZAI_BRANCH="${ZAI_BRANCH:-feat/self-queue-production}"
  ZAI_AGENTS="${ZAI_AGENTS:-planner,coder,reviewer}"
  ZAI_STAGE_FILE_LIST="${ZAI_STAGE_FILE_LIST:-configs/zai-self-dev.phase1.files}"
  ZAI_PR_TITLE="${ZAI_PR_TITLE:-feat: add production self-queue}"
  ZAI_PR_BODY="${ZAI_PR_BODY:-Adds durable local self-queue storage, task lifecycle commands, bounded worker behavior, retry/cancel/logs, TUI task status, tests, and operator docs.}"
  ZAI_MODEL_TIMEOUT_SECONDS="${ZAI_MODEL_TIMEOUT_SECONDS:-120}"
  APPLY="${APPLY:-0}"
  COMMIT="${COMMIT:-0}"
  CREATE_PR="${CREATE_PR:-0}"
}

clear_git_context() {
  unset GIT_DIR
  unset GIT_WORK_TREE
  unset GIT_INDEX_FILE
  unset GIT_COMMON_DIR
  unset GIT_CEILING_DIRECTORIES
}

repo_cd() {
  load_config
  clear_git_context
  cd "$ZAI_REPO_DIR" || die "Repo directory not found: $ZAI_REPO_DIR"
  git rev-parse --is-inside-work-tree >/dev/null 2>&1 || die "Not a git work tree: $ZAI_REPO_DIR"
}

activate_venv() {
  if [[ -f "$ZAI_VENV/bin/activate" ]]; then
    # shellcheck disable=SC1090
    source "$ZAI_VENV/bin/activate"
  elif [[ -f ".venv/bin/activate" ]]; then
    warn "Using repo-local .venv. Ensure it is ignored and never committed."
    # shellcheck disable=SC1091
    source ".venv/bin/activate"
  else
    warn "No venv found at $ZAI_VENV or .venv. Commands may use system Python."
  fi
}

require_apply() {
  [[ "$APPLY" == "1" ]] || die "This action mutates local repo state. Re-run with APPLY=1."
}

print_dirty_help() {
  cat <<'HELP'
Working tree is not clean.

Recommended safe cleanup:
  1. Restore accidental tracked deletions:
     git restore <tracked-file>

  2. Move local generated kit artifacts outside repo:
     mkdir -p /tmp/zai-coder-local-artifacts
     mv zai-coder-self-dev-kit.zip /tmp/zai-coder-local-artifacts/ 2>/dev/null || true
     mv zai-coder-self-dev-kit /tmp/zai-coder-local-artifacts/ 2>/dev/null || true
     mv release /tmp/zai-coder-local-artifacts/ 2>/dev/null || true

  3. Keep repo-local virtualenv untracked:
     grep -qxF '.venv/' .git/info/exclude || echo '.venv/' >> .git/info/exclude

  4. Recheck:
     git status --short
HELP
}

require_clean_tree() {
  local dirty
  dirty="$(git status --short)"
  if [[ -n "$dirty" ]]; then
    printf '%s\n' "$dirty"
    print_dirty_help
    die "Working tree is not clean."
  fi
}

cmd_doctor() {
  repo_cd
  log "Repo: $ZAI_REPO_DIR"
  log "Branch: $(git branch --show-current)"
  log "HEAD: $(git rev-parse --short HEAD)"
  log "Inside work tree: $(git rev-parse --is-inside-work-tree)"
  log "Bare repo: $(git rev-parse --is-bare-repository)"
  command -v python3 >/dev/null || die "python3 not found"
  command -v git >/dev/null || die "git not found"
  command -v gh >/dev/null || warn "gh not found; PR commands will be unavailable"
  if command -v zai-coder >/dev/null; then
    log "zai-coder: $(command -v zai-coder)"
    zai-coder --version || true
  else
    warn "zai-coder command not found in PATH"
  fi
  [[ -f "$ZAI_MASTER_PROMPT" ]] || warn "Missing master prompt: $ZAI_MASTER_PROMPT"
  [[ -f "$ZAI_PHASE_PROMPT" ]] || warn "Missing phase prompt: $ZAI_PHASE_PROMPT"
  [[ -f "$ZAI_STAGE_FILE_LIST" ]] || warn "Missing stage file list: $ZAI_STAGE_FILE_LIST"
  git status --short || true
}

cmd_sync() {
  repo_cd
  require_clean_tree
  log "Fetching origin"
  git fetch origin --prune --tags
  log "Switching to $ZAI_MAIN_BRANCH"
  git switch "$ZAI_MAIN_BRANCH"
  git pull --ff-only origin "$ZAI_MAIN_BRANCH"
  if command -v gh >/dev/null; then
    log "Open PRs"
    gh pr list --repo "$ZAI_REPO_FULL_NAME" --state open
  else
    warn "gh not found; skipping open PR check"
  fi
  git status --short
}

cmd_branch() {
  repo_cd
  require_apply
  require_clean_tree
  git fetch origin --prune --tags
  git switch "$ZAI_MAIN_BRANCH"
  git pull --ff-only origin "$ZAI_MAIN_BRANCH"
  if git show-ref --verify --quiet "refs/heads/$ZAI_BRANCH"; then
    log "Switching existing branch: $ZAI_BRANCH"
    git switch "$ZAI_BRANCH"
  else
    log "Creating branch: $ZAI_BRANCH"
    git switch -c "$ZAI_BRANCH"
  fi
}

cmd_prompt() {
  repo_cd
  [[ -f "$ZAI_MASTER_PROMPT" ]] || die "Missing master prompt: $ZAI_MASTER_PROMPT"
  [[ -f "$ZAI_PHASE_PROMPT" ]] || die "Missing phase prompt: $ZAI_PHASE_PROMPT"
  printf '### Master prompt: %s\n\n' "$ZAI_MASTER_PROMPT"
  sed -n '1,220p' "$ZAI_MASTER_PROMPT"
  printf '\n### Phase prompt: %s\n\n' "$ZAI_PHASE_PROMPT"
  sed -n '1,260p' "$ZAI_PHASE_PROMPT"
}

cmd_plan() {
  repo_cd
  log "Offline plan mode: printing prompts only. Use 'agent-plan' to call the configured model provider explicitly."
  cmd_prompt
}

cmd_agent_plan() {
  repo_cd
  activate_venv
  [[ -f "$ZAI_PHASE_PROMPT" ]] || die "Missing phase prompt: $ZAI_PHASE_PROMPT"
  local task_text
  task_text="Read $ZAI_MASTER_PROMPT for global safety rules. Then read $ZAI_PHASE_PROMPT and implement only that phase. Do not start any later phase. Produce a concise implementation plan first."
  log "Running model-backed zai-coder plan with timeout ${ZAI_MODEL_TIMEOUT_SECONDS}s"
  if command -v timeout >/dev/null; then
    timeout "$ZAI_MODEL_TIMEOUT_SECONDS" zai-coder plan --task "$task_text" --agents "$ZAI_AGENTS"
  else
    zai-coder plan --task "$task_text" --agents "$ZAI_AGENTS"
  fi
}

cmd_validate() {
  repo_cd
  activate_venv
  local commands=(
    "python3 -m pytest tests/test_tasks.py -q"
    "python3 -m pytest tests/test_self_queue_v014.py -q"
    "python3 -m pytest tests/test_task_queue_worker_v014.py -q"
    "python3 -m pytest tests/test_task_cli_v014.py -q"
    "python3 -m pytest tests/test_tui_task_panel_v014.py -q"
    "python3 -m pytest -q"
    "python3 -m compileall -q zai_coder"
    "make repo-check"
    "make secret-scan"
    "make stage-manifest-check"
    "./scripts/repo/check-generated-state.sh"
    "./scripts/repo/check-ci-pytest-setup.sh"
  )
  for command_text in "${commands[@]}"; do
    log "$command_text"
    bash -lc "$command_text"
  done
}

cmd_stage() {
  repo_cd
  require_apply
  [[ -f "$ZAI_STAGE_FILE_LIST" ]] || die "Missing stage list: $ZAI_STAGE_FILE_LIST"
  while IFS= read -r path; do
    [[ -z "$path" ]] && continue
    [[ "$path" =~ ^# ]] && continue
    if [[ -e "$path" ]]; then
      log "git add $path"
      git add "$path"
    else
      warn "Not found, skipping: $path"
    fi
  done < "$ZAI_STAGE_FILE_LIST"
  git status --short
}

cmd_commit() {
  repo_cd
  require_apply
  [[ "$COMMIT" == "1" ]] || die "Commit requires COMMIT=1."
  git diff --cached --quiet && die "No staged changes. Run APPLY=1 scripts/zai-self-dev.sh stage first."
  git commit -S -m "$ZAI_PR_TITLE"
}

cmd_pr() {
  repo_cd
  require_apply
  [[ "$CREATE_PR" == "1" ]] || die "PR creation requires CREATE_PR=1."
  command -v gh >/dev/null || die "gh not found"
  local current_branch
  current_branch="$(git branch --show-current)"
  [[ "$current_branch" == "$ZAI_BRANCH" ]] || die "Current branch '$current_branch' is not expected branch '$ZAI_BRANCH'"
  git push -u origin "$ZAI_BRANCH"
  gh pr create \
    --base "$ZAI_MAIN_BRANCH" \
    --head "$ZAI_BRANCH" \
    --draft \
    --title "$ZAI_PR_TITLE" \
    --body "$ZAI_PR_BODY"
}

cmd_local_exclude() {
  repo_cd
  require_apply
  local patterns=(
    ".venv/"
    "zai-coder-self-dev-kit.zip"
    "zai-coder-self-dev-kit/"
    "release/"
  )
  for pattern in "${patterns[@]}"; do
    grep -qxF "$pattern" .git/info/exclude || echo "$pattern" >> .git/info/exclude
  done
  log "Updated .git/info/exclude with local-only generated paths"
}

cmd_status() {
  repo_cd
  log "Branch: $(git branch --show-current)"
  log "HEAD: $(git rev-parse --short HEAD)"
  git status --short
  if command -v gh >/dev/null; then
    gh pr list --repo "$ZAI_REPO_FULL_NAME" --state open
  fi
}

usage() {
  cat <<'USAGE'
Usage:
  scripts/zai-self-dev.sh doctor
  scripts/zai-self-dev.sh sync
  scripts/zai-self-dev.sh branch         # requires APPLY=1
  scripts/zai-self-dev.sh prompt
  scripts/zai-self-dev.sh plan           # offline; prints prompts only
  scripts/zai-self-dev.sh agent-plan     # explicit model/provider call
  scripts/zai-self-dev.sh validate
  scripts/zai-self-dev.sh stage          # requires APPLY=1
  scripts/zai-self-dev.sh commit         # requires APPLY=1 COMMIT=1
  scripts/zai-self-dev.sh pr             # requires APPLY=1 CREATE_PR=1
  scripts/zai-self-dev.sh local-exclude  # requires APPLY=1
  scripts/zai-self-dev.sh status
USAGE
}

main() {
  local cmd="${1:-}"
  case "$cmd" in
    doctor) cmd_doctor ;;
    sync) cmd_sync ;;
    branch) cmd_branch ;;
    prompt) cmd_prompt ;;
    plan) cmd_plan ;;
    agent-plan) cmd_agent_plan ;;
    validate) cmd_validate ;;
    stage) cmd_stage ;;
    commit) cmd_commit ;;
    pr) cmd_pr ;;
    local-exclude) cmd_local_exclude ;;
    status) cmd_status ;;
    ""|-h|--help|help) usage ;;
    *) usage; die "Unknown command: $cmd" ;;
  esac
}

main "$@"
