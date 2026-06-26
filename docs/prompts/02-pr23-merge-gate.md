# Prompt: PR #23 Merge Gate — v0.1.4 Planning

```text
You are working locally in:

/home/zeazdev/zai-coder

Phase:
PR #23 Final Review and Merge Gate — v0.1.4 Planning Baseline

Goal:
Review and merge the v0.1.4 planning PR. This phase should merge planning docs only. No implementation, version bump, tag, release, asset upload, or release-state mutation.

Expected branch:
- chore/prepare-v0.1.4-planning

Expected files:
- docs/release/V0.1.4_PLANNING.md
- docs/release/V0.1.4_TASK_CHECKLIST.md
- docs/release/V0.1.4_INITIAL_ROADMAP.md

Critical rules:
- Do not rewrite history.
- Do not force push.
- Do not push directly to main.
- Do not use git add .
- Do not use git add -A
- Do not use --no-verify
- No version bump.
- No tag/release/asset mutation.
- No generated runtime state committed.

Run:

cd /home/zeazdev/zai-coder

git fetch origin --prune --tags
git switch chore/prepare-v0.1.4-planning
git pull --ff-only origin chore/prepare-v0.1.4-planning
git status --short
git diff --stat origin/main...HEAD
git diff --name-status origin/main...HEAD

sed -n '1,360p' docs/release/V0.1.4_PLANNING.md
sed -n '1,360p' docs/release/V0.1.4_TASK_CHECKLIST.md
sed -n '1,260p' docs/release/V0.1.4_INITIAL_ROADMAP.md

python3 -m compileall -q zai_coder
python3 -m pytest -q
make repo-check
make secret-scan
make stage-manifest-check
./scripts/repo/check-generated-state.sh
./scripts/repo/check-ci-pytest-setup.sh

git status --short

gh pr view 23 --repo cvsz/zai-coder --json isDraft,mergeable,headRefOid,baseRefOid,title,url

If checks pass:

gh pr ready 23 --repo cvsz/zai-coder || true
gh pr merge 23 --repo cvsz/zai-coder --merge --delete-branch

git fetch origin --prune --tags
git switch main
git pull --ff-only origin main
python3 -m pytest -q
make repo-check

Report:
1. PR ready status
2. merge commit
3. main HEAD
4. version remains 0.1.3
5. docs merged
6. validation result
7. branch deleted yes/no
8. next recommended implementation branch
```
