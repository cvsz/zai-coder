# Prompt: v0.1.4 Installer / Update / Uninstall Reliability

```text
You are working locally in:

/home/zeazdev/zai-coder

Phase:
v0.1.4 Implementation PR — Installer, Update, and Uninstall Reliability

Branch:
test/v0.1.4-installer-reliability

Goal:
Improve local installer/update/uninstall confidence with idempotency tests, failure-mode checks, and clearer recovery documentation. Keep all behavior local-first and safe.

Critical rules:
- No version bump.
- No tag/release/asset mutation.
- No direct main commit.
- Do not run destructive install commands against the real system without isolation.
- Use temporary directories for tests.
- Do not commit generated runtime state.
- Stage exact files only.

Steps:

cd /home/zeazdev/zai-coder

git fetch origin --prune --tags
git switch main
git pull --ff-only origin main
git status --short
git switch -c test/v0.1.4-installer-reliability

Inspect install/update/uninstall scripts:

find . -maxdepth 4 -type f | sort | grep -E 'install|uninstall|update|post-install|setup|bootstrap' || true
grep -R "install-local\|uninstall\|post-install\|update\|bootstrap\|PREFIX\|HOME" -n scripts tests docs Makefile 2>/dev/null | head -420

Add tests for:
- installer script exists and is executable
- uninstall script exists and is executable
- post-install check exists and is executable
- dry-run or temp-dir behavior if available
- idempotency where safe to simulate
- failure output is clear

Recommended files:
- tests/test_installer_reliability_v014.py
- docs/ops/install-recovery.md
- scripts only if a small safe fix is needed

Validation:

python3 -m pytest tests/test_installer_reliability_v014.py -q
python3 -m pytest -q
python3 -m compileall -q zai_coder
make repo-check
make secret-scan
make stage-manifest-check
./scripts/repo/check-generated-state.sh
./scripts/repo/check-ci-pytest-setup.sh

git status --short

git add tests/test_installer_reliability_v014.py
git add docs/ops/install-recovery.md
# add exact installer script files only if changed

git commit -S -m "test: harden installer reliability"
git push -u origin test/v0.1.4-installer-reliability

gh pr create \
  --base main \
  --head test/v0.1.4-installer-reliability \
  --draft \
  --title "test: harden installer reliability" \
  --body "Adds v0.1.4 installer/update/uninstall reliability coverage and recovery documentation."

Report:
1. branch
2. installer inventory
3. tests added
4. docs added
5. targeted validation
6. full validation
7. generated-file exclusion
8. commit hash
9. draft PR URL
```
