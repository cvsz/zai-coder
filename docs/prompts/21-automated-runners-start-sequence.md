# Prompt: Automated Runners Start Sequence

```text
You are working locally in:

/home/zeazdev/zai-coder

Phase:
Operational Start Prompt — Automated Agent Runners Sequence

Purpose:
Use this prompt before starting any automated agent runner implementation. It establishes a safe baseline, confirms release state, prevents generated-state drift, and chooses the next PR from the approved sequence.

Critical rules:
- Do not rewrite history.
- Do not force push.
- Do not push directly to main.
- Do not use git add .
- Do not use git add -A
- Do not use --no-verify.
- Do not bump version unless explicitly in release-candidate phase.
- Do not create tags unless explicitly in publish phase.
- Do not publish or mutate GitHub releases unless explicitly in publish phase.
- Do not commit generated state, runtime DBs, caches, logs, dist artifacts, evidence/export JSON, status.txt, or checkpoints.
- Use one small PR per feature.
- Stage exact files only.

Step 1: Sync and inspect baseline

cd /home/zeazdev/zai-coder

git fetch origin --prune --tags
git switch main
git pull --ff-only origin main
git status --short
git log -24 --oneline --decorate

Step 2: Verify package and release state

python3 - <<'PY'
import tomllib
from pathlib import Path

data = tomllib.loads(Path('pyproject.toml').read_text())
print(data['project']['version'])
assert data['project']['version'] == '0.1.3'
PY

python3 - <<'PY'
import zai_coder
print(zai_coder.__version__)
assert zai_coder.__version__ == '0.1.3'
PY

git tag -v v0.1.3 || true
gh release view v0.1.3 --repo cvsz/zai-coder --json tagName,name,isDraft,isPrerelease,url,assets,targetCommitish

Step 3: Clean working tree check

git status --short

If any local modifications exist, inspect before branching:

git diff --stat
git diff -- requirements-dev.txt || true

Do not carry unrelated local changes into the new PR.

Step 4: Run guardrails

python3 -m pytest -q
python3 -m compileall -q zai_coder
make repo-check
make secret-scan
make stage-manifest-check
./scripts/repo/check-generated-state.sh
./scripts/repo/check-ci-pytest-setup.sh

Step 5: Choose next PR

Approved sequence:
1. test/v0.1.4-safe-runner-policy
2. chore/v0.1.4-feature-registry
3. feat/v0.1.4-toolsets-skills-context
4. feat/v0.1.4-checkpoints-scheduler
5. feat/v0.1.4-subagent-runner-orchestration
6. feat/v0.1.4-provider-mcp-plugins
7. docs/v0.1.4-media-browser-voice-vision-plan
8. feat/v0.1.4-api-server-openai-compat
9. docs/automated-agent-runners-master-plan

Start with the earliest unmerged PR in this sequence.

Step 6: Branch naming rules

Use:
- test/ for test-only hardening
- chore/ for registries/docs/product metadata
- feat/ for new implementation
- fix/ for correctness bug fixes
- docs/ for planning-only changes

Step 7: PR creation rules

All PRs must be draft first:

gh pr create \
  --base main \
  --head <branch> \
  --draft \
  --title "<title>" \
  --body "<scope summary>"

Step 8: Final report format

Report:
1. selected prompt file
2. branch
3. baseline main commit
4. release state result
5. local changes handled
6. files changed
7. targeted validation
8. full validation
9. generated-file exclusion
10. commit hash
11. draft PR URL
12. next recommended PR
```
