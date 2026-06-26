# Prompt: Toolsets, Skills, and Context System

```text
You are working locally in:

/home/zeazdev/zai-coder

Phase:
v0.1.4+ Implementation PR — Toolsets, Skills, and Context System

Branch:
feat/v0.1.4-toolsets-skills-context

Goal:
Add a safe, local-first foundation for toolsets, skill loading, context files, and context references. This must preserve safety policy gates and avoid external network behavior by default.

Critical rules:
- No version bump.
- No tag/release/asset mutation.
- No direct main commit.
- Do not weaken safety policy.
- Do not add external web fetching unless behind a disabled-by-default provider flag.
- Do not read secrets or .env through context references.
- Do not commit generated state.
- Stage exact files only.

Step 1: Sync baseline

cd /home/zeazdev/zai-coder

git fetch origin --prune --tags
git switch main
git pull --ff-only origin main
git status --short

git switch -c feat/v0.1.4-toolsets-skills-context

Step 2: Inspect current registry/skills/assets

find assets skills docs -maxdepth 4 -type f | sort | head -500
grep -R "JsonRegistry\|SkillManifest\|skills\|agents\|SOUL\|AGENTS.md\|CLAUDE.md\|cursorrules\|context" -n zai_coder docs tests assets skills 2>/dev/null | head -600

Step 3: Add toolset registry foundation

Recommended files:
- zai_coder/core/toolsets.py
- tests/test_toolsets_v014.py
- docs/ops/toolsets.md

Toolset model:
- id
- label
- description
- enabled_by_default
- allowed_commands
- blocked_commands
- requires_integration
- risk_level

Initial toolsets:
- read_only
- test
- build
- patch
- operator
- locked_down
- research_local
- media_local
- server_local

Step 4: Add context file discovery

Recommended files:
- zai_coder/core/context_files.py
- tests/test_context_files_v014.py
- docs/ops/context-files.md

Supported context files:
- .zai.md
- .hermes.md
- AGENTS.md
- CLAUDE.md
- SOUL.md
- .cursorrules

Rules:
- local files only
- workspace-bound path resolution
- max file size limit
- deterministic load order
- redaction before display/logging
- no secret files

Step 5: Add local context references

Recommended files:
- zai_coder/core/context_refs.py
- tests/test_context_refs_v014.py
- docs/ops/context-references.md

Supported references for first PR:
- @file:path
- @dir:path
- @git:status
- @git:diff

Explicitly defer:
- @url until provider-gated web adapter exists
- remote git references
- binary files
- secret files

Step 6: CLI integration

Add only if small and safe:
- zai-coder context list
- zai-coder context show
- zai-coder context refs "..."

If CLI integration is too large, ship library + tests + docs first.

Step 7: Validation

python3 -m pytest tests/test_toolsets_v014.py tests/test_context_files_v014.py tests/test_context_refs_v014.py -q
python3 -m pytest -q
python3 -m compileall -q zai_coder
make repo-check
make secret-scan
make stage-manifest-check
./scripts/repo/check-generated-state.sh
./scripts/repo/check-ci-pytest-setup.sh

Step 8: Stage exact files only

git add zai_coder/core/toolsets.py
git add zai_coder/core/context_files.py
git add zai_coder/core/context_refs.py
git add tests/test_toolsets_v014.py
git add tests/test_context_files_v014.py
git add tests/test_context_refs_v014.py
git add docs/ops/toolsets.md
git add docs/ops/context-files.md
git add docs/ops/context-references.md

# Add exact CLI files only if changed.

Step 9: Commit and PR

git commit -S -m "feat: add toolsets and local context system"
git push -u origin feat/v0.1.4-toolsets-skills-context

gh pr create \
  --base main \
  --head feat/v0.1.4-toolsets-skills-context \
  --draft \
  --title "feat: add toolsets and local context system" \
  --body "Adds local-first toolset metadata, context file discovery, and safe local context references."

Report:
1. branch
2. toolsets added
3. context files supported
4. context refs supported
5. CLI integration yes/no
6. validation result
7. generated-file exclusion
8. commit hash
9. draft PR URL
```
