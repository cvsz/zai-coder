# Prompt: v0.1.4 Planning Baseline

```text
You are working locally in:

/home/zeazdev/zai-coder

Phase:
v0.1.4 Planning Baseline — Post-v0.1.3 Roadmap and Task Checklist

Goal:
Create the v0.1.4 planning baseline only. Do not implement features. Do not bump the package version. Do not create tags, GitHub releases, artifacts, or publish anything.

Current state:
- v0.1.3 release complete.
- PR #21 generated-state guardrails merged.
- PR #22 release-process guardrails merged.
- Current package version remains 0.1.3.
- Expected validation baseline: 477 passed.

Critical rules:
- No direct main commits.
- No version bump.
- No tag/release/asset mutation.
- No generated runtime state committed.
- Stage exact planning files only.

Steps:

cd /home/zeazdev/zai-coder

git fetch origin --prune --tags
git switch main
git pull --ff-only origin main
git status --short

git switch -c chore/prepare-v0.1.4-planning

Create:
- docs/release/V0.1.4_PLANNING.md
- docs/release/V0.1.4_TASK_CHECKLIST.md
- docs/release/V0.1.4_INITIAL_ROADMAP.md

Planning theme:
Enterprise Hardening and Operator Experience

Workstreams:
1. CLI operator UX and diagnostics.
2. Policy and safe-runner hardening.
3. Installer/update/uninstall reliability.
4. Test coverage and CI reliability.
5. Release automation guardrail improvements.
6. Documentation and examples polish.
7. Optional server/API diagnostics.
8. Package metadata and install verification.

Validation:

python3 -m compileall -q zai_coder
python3 -m pytest -q
make repo-check
make secret-scan
make stage-manifest-check
./scripts/repo/check-generated-state.sh
./scripts/repo/check-ci-pytest-setup.sh

git status --short

git add docs/release/V0.1.4_PLANNING.md
git add docs/release/V0.1.4_TASK_CHECKLIST.md
git add docs/release/V0.1.4_INITIAL_ROADMAP.md
git commit -S -m "chore: plan v0.1.4"
git push -u origin chore/prepare-v0.1.4-planning

gh pr create \
  --base main \
  --head chore/prepare-v0.1.4-planning \
  --draft \
  --title "chore: plan v0.1.4" \
  --body-file docs/release/V0.1.4_PLANNING.md

Report:
1. branch
2. main baseline
3. version verification
4. planning docs created
5. validation result
6. generated-file exclusion result
7. commit hash
8. draft PR URL
9. recommended first implementation PR
```
