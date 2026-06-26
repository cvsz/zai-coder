# Prompt: Checkpoints, Rollback, and Local Scheduler

```text
You are working locally in:

/home/zeazdev/zai-coder

Phase:
v0.1.4+ Implementation PR — Checkpoints, Rollback, and Local Scheduler

Branch:
feat/v0.1.4-checkpoints-scheduler

Goal:
Improve checkpoint and rollback UX, then add a local-first scheduled task foundation. The scheduler must be safe-runner-gated, local-only by default, and paused/disabled by default unless explicitly enabled.

Critical rules:
- No version bump.
- No tag/release/asset mutation.
- No direct main commit.
- Do not implement uncontrolled background execution.
- Do not add daemon/autostart behavior.
- Do not weaken safe runner.
- Do not commit generated task DBs, logs, runtime JSON, or checkpoints.
- Stage exact files only.

Step 1: Sync baseline

cd /home/zeazdev/zai-coder

git fetch origin --prune --tags
git switch main
git pull --ff-only origin main
git status --short

git switch -c feat/v0.1.4-checkpoints-scheduler

Step 2: Inspect existing checkpoint and patch code

grep -R "PatchRuntime\|checkpoint\|rollback\|scheduler\|cron\|job" -n zai_coder tests docs scripts 2>/dev/null | head -500
sed -n '1,240p' zai_coder/core/patcher.py

Step 3: Checkpoint/rollback UX

Recommended files:
- zai_coder/core/checkpoints.py
- tests/test_checkpoints_v014.py
- docs/ops/checkpoints-and-rollback.md

Add functions/classes for:
- list_checkpoints(workspace)
- checkpoint_metadata(path)
- restore_checkpoint(workspace, checkpoint_id, dry_run=True)
- delete_checkpoint(workspace, checkpoint_id, dry_run=True)

Rules:
- workspace-bound paths only
- dry-run default for restore/delete
- never restore over secret files without explicit manual flag
- do not commit checkpoint artifacts
- path traversal blocked

Optional CLI:
- zai-coder checkpoint list
- zai-coder checkpoint show <id>
- zai-coder checkpoint restore <id> --dry-run
- zai-coder checkpoint restore <id> --apply

Step 4: Local scheduler foundation

Recommended files:
- zai_coder/core/scheduler.py
- tests/test_scheduler_v014.py
- docs/ops/local-scheduler.md

Scheduler model:
- job id
- name
- command or prompt reference
- schedule expression
- enabled false by default
- toolset/profile
- workspace
- created_at
- last_run_at
- last_result

First PR may only add data model and dry-run executor.
Do not add resident daemon or background process.

CLI, if small:
- zai-coder schedule list
- zai-coder schedule add --name ... --cron ... --command ... --disabled
- zai-coder schedule run-now <id> --dry-run
- zai-coder schedule enable <id>
- zai-coder schedule disable <id>

Step 5: Validation

python3 -m pytest tests/test_checkpoints_v014.py tests/test_scheduler_v014.py -q
python3 -m pytest -q
python3 -m compileall -q zai_coder
make repo-check
make secret-scan
make stage-manifest-check
./scripts/repo/check-generated-state.sh
./scripts/repo/check-ci-pytest-setup.sh

git status --short

Step 6: Stage exact files only

git add zai_coder/core/checkpoints.py
git add zai_coder/core/scheduler.py
git add tests/test_checkpoints_v014.py
git add tests/test_scheduler_v014.py
git add docs/ops/checkpoints-and-rollback.md
git add docs/ops/local-scheduler.md

# Add exact CLI files only if changed.

Step 7: Commit and PR

git commit -S -m "feat: add checkpoint rollback and scheduler foundation"
git push -u origin feat/v0.1.4-checkpoints-scheduler

gh pr create \
  --base main \
  --head feat/v0.1.4-checkpoints-scheduler \
  --draft \
  --title "feat: add checkpoint rollback and scheduler foundation" \
  --body "Adds checkpoint/rollback UX and a disabled-by-default local scheduler foundation."

Report:
1. branch
2. checkpoint behavior added
3. scheduler behavior added
4. CLI commands added or deferred
5. targeted validation
6. full validation
7. generated-file exclusion
8. commit hash
9. draft PR URL
```
