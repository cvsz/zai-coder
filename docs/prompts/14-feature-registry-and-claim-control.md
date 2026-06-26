# Prompt: Feature Registry and Claim-Control Matrix

```text
You are working locally in:

/home/zeazdev/zai-coder

Phase:
v0.1.4 Implementation PR — Product Feature Registry and Claim Control

Branch:
chore/v0.1.4-feature-registry

Goal:
Add a source-of-truth product feature registry that classifies ZAI Coder capabilities as available, partial, planned, requires_integration, or do_not_claim. Use it to align product copy, tier planning, and Hermes-style feature roadmap without overclaiming unsupported features.

Critical rules:
- No version bump.
- No tag/release/asset mutation.
- No direct main commit.
- Do not claim features that do not exist in code.
- Do not add vendor-specific API promises unless provider integration exists.
- Do not commit generated state.
- Stage exact files only.

Feature status enum:
- available: implemented and tested enough to mention as supported.
- partial: foundation exists, but product claim must be cautious.
- planned: roadmap item, not implemented.
- requires_integration: requires external provider, OAuth, API keys, MCP server, browser service, or cloud infrastructure.
- do_not_claim: marketing claim is unsafe or unsupported until real infra exists.

Step 1: Sync baseline

cd /home/zeazdev/zai-coder

git fetch origin --prune --tags
git switch main
git pull --ff-only origin main
git status --short

git switch -c chore/v0.1.4-feature-registry

Step 2: Inspect current features

grep -R "ToolRuntime\|SafetyPolicy\|MemoryStore\|LocalRAG\|PatchRuntime\|ModelRouter\|run_server\|generate_svg_image\|generate_voice_wav\|cmd_" -n zai_coder tests docs scripts 2>/dev/null | head -600

Step 3: Add source files

Create:
- zai_coder/product/__init__.py
- zai_coder/product/features.py

Feature registry should include:
- local_cli
- safe_runner
- policy_guards
- local_rag
- local_memory
- patch_checkpoints
- basic_api_server
- basic_media_generation
- provider_routing
- fallback_provider
- skills_marketplace
- automated_agent_runners
- scheduled_tasks
- subagent_delegation
- browser_automation
- mcp_integration
- slack_connector
- google_workspace_connector
- credential_pools
- prompt_caching
- external_memory_providers
- ide_acp
- pwa_mobile_desktop
- priority_access
- twenty_x_usage

Each record should include:
- id
- label
- status
- tier_hint
- claim
- evidence_path optional
- notes

Step 4: Add tests

Create:
- tests/test_feature_registry_v014.py

Tests should assert:
- every feature has valid status
- do_not_claim features cannot have claim text that sounds available
- requires_integration features mention integration/provider/API/OAuth
- available features have at least one evidence path or implementation note
- tier names are from Free, Pro, Max, Enterprise, Internal, Roadmap

Step 5: Add docs

Create:
- docs/product/FEATURE_MATRIX.md
- docs/product/TIER_PLAN.md
- docs/product/CLAIM_CONTROL.md

Docs must clearly separate:
- available now
- partial/beta
- planned
- requires integration
- do not claim

Step 6: Validation

python3 -m pytest tests/test_feature_registry_v014.py -q
python3 -m pytest -q
python3 -m compileall -q zai_coder
make repo-check
make secret-scan
make stage-manifest-check
./scripts/repo/check-generated-state.sh
./scripts/repo/check-ci-pytest-setup.sh

git status --short

Step 7: Stage exact files only

git add zai_coder/product/__init__.py
git add zai_coder/product/features.py
git add tests/test_feature_registry_v014.py
git add docs/product/FEATURE_MATRIX.md
git add docs/product/TIER_PLAN.md
git add docs/product/CLAIM_CONTROL.md

Step 8: Commit and PR

git commit -S -m "chore: add product feature registry"
git push -u origin chore/v0.1.4-feature-registry

gh pr create \
  --base main \
  --head chore/v0.1.4-feature-registry \
  --draft \
  --title "chore: add product feature registry" \
  --body "Adds a feature registry and claim-control docs so product copy stays aligned with implemented capabilities."

Report:
1. branch
2. baseline
3. feature count
4. statuses represented
5. docs created
6. tests added
7. validation result
8. commit hash
9. draft PR URL
```
