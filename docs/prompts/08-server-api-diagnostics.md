# Prompt: v0.1.4 Optional Server/API Diagnostics

```text
You are working locally in:

/home/zeazdev/zai-coder

Phase:
v0.1.4 Optional Implementation PR — Server/API Diagnostics

Branch:
test/v0.1.4-server-api-diagnostics

Goal:
If server/API mode is actively supported, improve diagnostics and tests for local server health, status, startup/shutdown, config, and ports. If server/API mode is not active, produce an inventory doc and skip behavioral changes.

Critical rules:
- No version bump.
- No tag/release/asset mutation.
- No direct main commit.
- Do not run public network services.
- Use localhost only.
- Do not commit generated runtime state.
- Stage exact files only.

Steps:

cd /home/zeazdev/zai-coder

git fetch origin --prune --tags
git switch main
git pull --ff-only origin main
git status --short
git switch -c test/v0.1.4-server-api-diagnostics

Inventory server/API code:

find zai_coder tests docs scripts -maxdepth 4 -type f | sort | grep -E 'server|api|serve|route|health|status|fastapi|flask|http' || true
grep -R "serve\|server\|health\|status\|FastAPI\|Flask\|uvicorn\|localhost\|port" -n zai_coder tests docs scripts 2>/dev/null | head -420

Decision:
- If server/API mode exists, add focused tests and docs.
- If not, create docs/ops/server-api-diagnostics-inventory.md and stop without adding dead code.

Recommended files if active:
- tests/test_server_api_diagnostics_v014.py
- docs/ops/server-api-diagnostics.md
- relevant server source only if small diagnostics fix is needed

Validation:

python3 -m pytest tests/test_server_api_diagnostics_v014.py -q || true
python3 -m pytest -q
python3 -m compileall -q zai_coder
make repo-check
make secret-scan
make stage-manifest-check
./scripts/repo/check-generated-state.sh
./scripts/repo/check-ci-pytest-setup.sh

git status --short

git add docs/ops/server-api-diagnostics.md 2>/dev/null || true
git add docs/ops/server-api-diagnostics-inventory.md 2>/dev/null || true
git add tests/test_server_api_diagnostics_v014.py 2>/dev/null || true
# add exact server source files only if changed

git commit -S -m "test: add server API diagnostics coverage"
git push -u origin test/v0.1.4-server-api-diagnostics

gh pr create \
  --base main \
  --head test/v0.1.4-server-api-diagnostics \
  --draft \
  --title "test: add server API diagnostics coverage" \
  --body "Adds or inventories v0.1.4 server/API diagnostics without changing release state."

Report:
1. branch
2. server/API active yes/no
3. files changed
4. tests added yes/no
5. validation result
6. generated-file exclusion
7. commit hash
8. draft PR URL
```
