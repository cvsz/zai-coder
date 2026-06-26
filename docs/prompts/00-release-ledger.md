# Prompt: Release Ledger and Operating Rules

Use this prompt before starting any new ZAI Coder release or hardening phase.

```text
You are working locally in:

/home/zeazdev/zai-coder

Phase:
Release Ledger Verification and Operating Rules

Current verified state:
- v0.1.3 release is complete.
- v0.1.3 tag exists and is GPG verified.
- v0.1.3 GitHub release is published.
- All 5 expected release assets are attached.
- PR #21 merged generated-state guardrails.
- PR #22 merged release-process guardrails.
- Current package version remains 0.1.3.
- Expected validation baseline after PR #22: 477 tests passed.

Goal:
Verify the repository is clean, release state is intact, guardrails are active, and the next branch can be created safely.

Critical rules:
- Do not rewrite history.
- Do not force push.
- Do not push directly to main.
- Do not use git add .
- Do not use git add -A
- Do not use --no-verify
- Do not mutate tags or GitHub releases unless this is an explicit publish prompt.
- Do not commit generated runtime state.

Run:

cd /home/zeazdev/zai-coder

git fetch origin --prune --tags
git switch main
git pull --ff-only origin main
git status --short
git log -18 --oneline --decorate

python3 - <<'PY'
import tomllib
from pathlib import Path

data = tomllib.loads(Path('pyproject.toml').read_text())
assert data['project']['version'] == '0.1.3'
print(data['project']['version'])
PY

python3 - <<'PY'
import zai_coder
assert getattr(zai_coder, '__version__', None) == '0.1.3'
print(zai_coder.__version__)
PY

git tag -v v0.1.3 || true
gh release view v0.1.3 --repo cvsz/zai-coder --json tagName,name,isDraft,isPrerelease,url,assets,targetCommitish

./scripts/repo/check-generated-state.sh
./scripts/repo/check-ci-pytest-setup.sh
make repo-check
make secret-scan
make stage-manifest-check
python3 -m pytest -q

Report:
1. current branch
2. current HEAD
3. version result
4. release tag verification result
5. GitHub release verification result
6. guardrail result
7. validation result
8. generated-file exclusion result
```
