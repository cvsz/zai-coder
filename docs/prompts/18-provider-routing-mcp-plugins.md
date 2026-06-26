# Prompt: Provider Routing, MCP, and Plugins

```text
You are working locally in:

/home/zeazdev/zai-coder

Phase:
v0.1.4+ Implementation PR — Provider Routing, MCP, and Plugin Foundation

Branch:
feat/v0.1.4-provider-mcp-plugins

Goal:
Improve provider routing and add a plugin/MCP foundation without enabling unsafe external tools by default. External integrations must be explicit, configured, filtered, and auditable.

Critical rules:
- No version bump.
- No tag/release/asset mutation.
- No direct main commit.
- Do not store credentials in git.
- Do not add real API keys.
- Do not enable external MCP servers by default.
- Do not allow unfiltered tools from external servers.
- Do not commit generated plugin caches/logs.
- Stage exact files only.

Step 1: Sync baseline

cd /home/zeazdev/zai-coder

git fetch origin --prune --tags
git switch main
git pull --ff-only origin main
git status --short

git switch -c feat/v0.1.4-provider-mcp-plugins

Step 2: Inspect provider and tool code

grep -R "ModelRouter\|provider_from_config\|OpenAICompatibleProvider\|ToolRuntime\|plugin\|mcp\|credential\|fallback" -n zai_coder tests docs scripts 2>/dev/null | head -600

Step 3: Provider routing improvements

Recommended files:
- zai_coder/core/provider_routing.py
- tests/test_provider_routing_v014.py
- docs/ops/provider-routing.md

Routing features:
- provider id
- provider type
- priority
- enabled
- requires_api_key
- env var name
- supports_text
- supports_vision
- supports_audio
- supports_tools
- max_tokens_hint
- cost_tier hint
- fallback order

Do not add actual provider calls beyond existing OpenAI-compatible provider unless scoped and tested.

Step 4: Plugin registry foundation

Recommended files:
- zai_coder/core/plugins.py
- tests/test_plugins_v014.py
- docs/ops/plugins.md

Plugin manifest fields:
- id
- name
- type: toolset, hook, memory_provider, context_engine, mcp_adapter
- enabled false by default
- risk_level
- allowed_tools
- blocked_tools
- config_schema

Step 5: MCP adapter interface

Recommended files:
- zai_coder/mcp/__init__.py
- zai_coder/mcp/adapter.py
- tests/test_mcp_adapter_v014.py
- docs/ops/mcp.md

MCP rules:
- stdio/http transports are planned but disabled by default
- tool filtering required
- external server config cannot include secrets in repo
- all tool calls pass through SafetyPolicy/ToolRuntime equivalent
- log only redacted metadata

Step 6: Validation

python3 -m pytest tests/test_provider_routing_v014.py tests/test_plugins_v014.py tests/test_mcp_adapter_v014.py -q
python3 -m pytest -q
python3 -m compileall -q zai_coder
make repo-check
make secret-scan
make stage-manifest-check
./scripts/repo/check-generated-state.sh
./scripts/repo/check-ci-pytest-setup.sh

git status --short

Step 7: Stage exact files only

git add zai_coder/core/provider_routing.py
git add zai_coder/core/plugins.py
git add zai_coder/mcp/__init__.py
git add zai_coder/mcp/adapter.py
git add tests/test_provider_routing_v014.py
git add tests/test_plugins_v014.py
git add tests/test_mcp_adapter_v014.py
git add docs/ops/provider-routing.md
git add docs/ops/plugins.md
git add docs/ops/mcp.md

Step 8: Commit and PR

git commit -S -m "feat: add provider routing and plugin foundations"
git push -u origin feat/v0.1.4-provider-mcp-plugins

gh pr create \
  --base main \
  --head feat/v0.1.4-provider-mcp-plugins \
  --draft \
  --title "feat: add provider routing and plugin foundations" \
  --body "Adds provider routing metadata, plugin registry foundations, and a disabled-by-default MCP adapter interface."

Report:
1. branch
2. provider routing fields
3. plugin manifest fields
4. MCP safety rules
5. validation result
6. generated-file exclusion
7. commit hash
8. draft PR URL
```
