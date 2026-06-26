# Prompt: API Server, IDE, and OpenAI-Compatible Endpoint

```text
You are working locally in:

/home/zeazdev/zai-coder

Phase:
v0.1.4+ Implementation PR — API Server, IDE, and OpenAI-Compatible Endpoint

Branch:
feat/v0.1.4-api-server-openai-compat

Goal:
Harden the local API server and plan OpenAI-compatible endpoint behavior for use with local frontends and future IDE integrations. Fix version drift and keep remote bind disabled by default.

Critical rules:
- No version bump.
- No tag/release/asset mutation.
- No direct main commit.
- Do not expose remote network binding by default.
- Do not add authentication bypasses.
- Do not claim full OpenAI compatibility unless implemented and tested.
- Do not commit generated server logs or runtime DBs.
- Stage exact files only.

Step 1: Sync baseline

cd /home/zeazdev/zai-coder

git fetch origin --prune --tags
git switch main
git pull --ff-only origin main
git status --short

git switch -c feat/v0.1.4-api-server-openai-compat

Step 2: Inspect server code

grep -R "run_server\|HTTPServer\|handle_get\|handle_post\|/version\|/ask\|/plan\|/run\|OpenAI-compatible\|chat/completions" -n zai_coder tests docs 2>/dev/null | head -600

Step 3: Fix version endpoint

Current risk to check:
- /version may be hard-coded and must align with zai_coder.__version__.

Recommended files:
- zai_coder/server/routes.py
- tests/test_server_version_v014.py
- docs/ops/server-api.md

Expected behavior:
- GET /version returns package version.
- GET /health returns ok.
- remote bind remains disabled unless config explicitly enables it.

Step 4: Add OpenAI-compatible plan

Create:
- docs/architecture/OPENAI_COMPATIBLE_API_PLAN.md

Plan endpoints:
- GET /v1/models
- POST /v1/chat/completions
- POST /v1/responses optional later

First implementation can be docs + tests for existing endpoints only. Do not claim full compatibility until endpoints exist.

Step 5: IDE integration plan

Create:
- docs/architecture/IDE_INTEGRATION_PLAN.md

Classify:
- planned: ACP-compatible editors
- requires_integration: VS Code, Zed, JetBrains adapters
- available: local server primitives only

Step 6: Validation

python3 -m pytest tests/test_server_version_v014.py -q
python3 -m pytest -q
python3 -m compileall -q zai_coder
make repo-check
make secret-scan
make stage-manifest-check
./scripts/repo/check-generated-state.sh
./scripts/repo/check-ci-pytest-setup.sh

git status --short

Step 7: Stage exact files only

git add zai_coder/server/routes.py
git add tests/test_server_version_v014.py
git add docs/ops/server-api.md
git add docs/architecture/OPENAI_COMPATIBLE_API_PLAN.md
git add docs/architecture/IDE_INTEGRATION_PLAN.md

Step 8: Commit and PR

git commit -S -m "fix: align server version endpoint"
git push -u origin feat/v0.1.4-api-server-openai-compat

gh pr create \
  --base main \
  --head feat/v0.1.4-api-server-openai-compat \
  --draft \
  --title "fix: align server version endpoint" \
  --body "Aligns the local server version endpoint and adds API/IDE compatibility planning docs."

Report:
1. branch
2. server version behavior
3. endpoints tested
4. OpenAI compatibility status
5. IDE integration status
6. validation result
7. generated-file exclusion
8. commit hash
9. draft PR URL
```
