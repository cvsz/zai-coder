# AGENTS.md

This is the root operating contract for Codex, Claude, Gemini, Cursor, OpenHands, and any other AI agent working in this repository.

Repository: `zai-coder`  
Workspace: `/home/zeazdev/zai-coder`  
Product: local-first AI coding and enterprise control-plane framework with Python core modules, optional production server extras, and an owned Open WebUI-based frontend under `web/`.

## Mission

Move ZAI Coder toward a Master Advanced Professional Enterprise-grade production-ready release without overstating readiness.

Use evidence from files, tests, scripts, docs, feature metadata, and release gates. Local release-ready and external production-ready are different states in this repo.

## Authority Order

When instructions conflict, use this order:

1. System and tool safety instructions.
2. This root `AGENTS.md`.
3. More specific nested agent files such as `.codex/AGENTS.md`.
4. Local skill/workflow files under `.agents/`, `.claude/`, and `skills/`.
5. Older roadmap or planning drafts.

Important override: Python source files in this repo use importable `snake_case.py` module names. Do not create hyphenated Python filenames even if an auto-generated skill mentions kebab-case.

## Current Truth Sources

- Canonical roadmap: `ROADMAP.md`.
- Release status: `FINAL_RELEASE_STATUS.md`, `FINAL_RELEASE_GATE_REPORT.md`, `FINAL_RELEASE_MANIFEST.json`.
- Feature metadata: `assets/**/*features.json`.
- Python implementation: `zai_coder/*`.
- Web implementation: `web/`.
- Web migration manifest: `web/src/lib/zai/migration-manifest.json`.
- Release and repository gates: `Makefile`, `scripts/repo/*`, `scripts/release/*`.
- CI baseline: `.github/workflows/ci.yml`.
- Codex ECC supplement: `.codex/AGENTS.md`.

Treat `docs/ROADMAPS.md` as a draft/reference if present. The root `ROADMAP.md` is canonical.

## Product Boundaries

ZAI Coder is intentionally local-first:

- Default behavior is dry-run-first.
- Apply-level actions require explicit `APPLY=1` or a documented approval path.
- Public/external go-live is blocked until runtime, gateway, auth, persistence, web CI, Cloudflare Access/DNS, and rollback gates pass together.
- Provider adapters and external actions are approval-gated. Do not post, publish, push, deploy, merge, open paid jobs, modify third-party resources, or change credentials without explicit user approval.

Never claim "production-ready" from local unit tests alone. Say "local release-ready" unless the external production gates are actually green.

## Development Rules

- Inspect before editing. Use `rg`, `rg --files`, `find`, `sed`, and targeted file reads.
- Preserve dirty worktree changes. Do not revert user changes unless explicitly asked.
- Keep edits scoped to the requested feature, file set, or release gate.
- Add or update tests with behavior changes.
- Prefer existing modules, scripts, patterns, and route conventions over new abstractions.
- For Python package code, use standard-library-first patterns unless the target surface already depends on optional extras.
- Keep public APIs deterministic and easy to test without external services.
- Validate inputs at system boundaries.
- Never hardcode secrets. Never read or print `.env` unless the user explicitly asks for a scoped key and it is safe to handle.
- Do not include `.env`, local databases, caches, release archives, or generated artifacts in source package claims.
- Do not use `git add .`, `git add -A`, `--no-verify`, force push, broad `rm -rf`, or pipe-to-shell install patterns.

## Python Core

The Python package is dependency-light by design:

- Base package metadata: `pyproject.toml`.
- Base runtime dependencies: none required.
- Optional TUI dependency: `textual`.
- Optional production server dependencies: `requirements-production.txt`.
- CLI entrypoint: `zai-coder = zai_coder.cli:main`.

Use these patterns:

- Modules live under `zai_coder/<domain>/`.
- Tests live under `tests/test_<domain>.py` or versioned equivalents.
- Use explicit dataclasses/models and plain dictionaries where existing code does.
- Keep command execution dry-run-safe and approval-aware.
- Export public helpers intentionally with `__all__` when surrounding modules do so.

## Web Surface

`web/` is an owned Open WebUI-based frontend, not just a random vendor dump.

Current ZAI-owned surface:

- `web/src/routes/(app)/zai/+page.svelte`
- `web/src/lib/zai/migration-manifest.json`
- `web/src/lib/zai/migration.ts`
- `web/src/lib/zai/openui.ts`
- `web/src/lib/components/zai/OpenUIRenderer.svelte`

Rules for web work:

- Keep the distinction between imported Open WebUI baseline and first-party ZAI code clear.
- Do not claim full web production readiness until install, lint, typecheck, test, build, accessibility, SBOM, license, and secret-scan gates are wired and passing.
- When touching framework/library APIs, use current documentation via Context7 before answering or changing code.
- Prefer the existing Svelte/Open WebUI patterns in `web/`; do not introduce a separate React app unless explicitly requested.

## Feature Map

The repo has feature-pack metadata for these production domains:

- Core local AI: `zai_coder/core`, `zai_coder/agents`, `zai_coder/skills`, `zai_coder/tui`, `zai_coder/evals`.
- Release and safety: `zai_coder/github_ready_core`, `zai_coder/deployment_core`, `zai_coder/final_enterprise_release_pack`, `scripts/repo`, `scripts/release`.
- Enterprise control plane: admin console, governance, compliance, reporting board pack, operations center, go-live command center.
- SaaS and tenancy: production SaaS core, multi-tenant control, billing usage enforcement, payment sandbox, customer portal.
- Automation runtime: execution runner, worker orchestration, agent runtime supervisor, self-healing operations.
- Integrations: production API gateway, real provider adapters, plugin connector hub, agent marketplace and skills, developer portal API docs.
- Operations: observability suite, backup/restore disaster recovery, security operations, quality assurance test lab, migration center, scalability planner.
- Product growth and content: feedback roadmap center, knowledge base help center, usage analytics, notification center, template content studio, team collaboration.
- Frontend: Open WebUI baseline plus ZAI command center and OpenUI renderer under `web/`.

For exact file-level inventory, use `ROADMAP.md` and `assets/**/*features.json`.

## Local Skills And Agent Files

Codex-facing skill:

- `.agents/skills/zai-coder/SKILL.md`
- `.agents/skills/zai-coder/agents/openai.yaml`

Claude-facing skill and commands:

- `.claude/skills/zai-coder/SKILL.md`
- `.claude/commands/feature-development.md`
- `.claude/commands/add-new-module-with-tests.md`
- `.claude/commands/repository-hardening-and-policy-update.md`

Repo skills:

- `skills/zai-coder/SKILL.md` for OpenUI/ZAI UX direction.
- `skills/hermes-skill-author/SKILL.md` for Hermes-compatible skill authoring.

Use these as workflow aids, not as permission to overclaim implementation state.

## Codex ECC Baseline

Treat `.codex/config.toml` as the project-local Codex baseline.

Managed MCP servers:

- GitHub
- Context7
- Exa
- Memory
- Playwright
- Sequential Thinking

The canonical Context7 section name is `[mcp_servers.context7]`; the launcher package is `@upstash/context7-mcp@latest`.

Multi-agent roles are configured under `.codex/agents/`:

- `explorer`: read-only evidence gathering.
- `reviewer`: correctness, security, regression, and missing-test review.
- `docs-researcher`: primary-doc and release-note verification.

## Context7 Rule

Use the `ctx7` CLI whenever the user asks about a library, framework, SDK, API, CLI tool, or cloud service.

Sequence:

1. `npx ctx7@latest library <name> "<full question>"`
2. Pick the best official/high-reputation ID.
3. `npx ctx7@latest docs <libraryId> "<full question>"`

Do not use Context7 for ordinary repo refactoring, business logic debugging, code review, or general programming concepts.

If Context7 fails because of quota, say so and suggest `npx ctx7@latest login` or `CONTEXT7_API_KEY`. If it fails because of DNS/network sandboxing and the docs are required for the task, rerun with the required network approval path.

## Validation Gates

Use the smallest relevant gate first, then broaden as risk increases.

Core gates:

```bash
python3 -m compileall -q zai_coder
python3 -m pytest -q
make repo-check
make secret-scan
make stage-manifest-check
make final-release-status APPLY=1
```

Release/source gates:

```bash
make verify-source-package
make release-checksums
make release-sbom
```

Web gates:

```bash
make web-check APPLY=1
make web-migration-report
```

Optional production runtime gate to add/maintain:

```bash
python3 -m pip install -r requirements-production.txt
python3 -m compileall -q zai_coder
```

Do not report a fully green finish if a relevant gate was skipped, unavailable, or blocked by missing optional dependencies.

## Common Workflows

Feature implementation:

1. Read the matching `assets/**/*features.json`, module directory, tests, docs, and scripts.
2. Update implementation and tests together.
3. Run the targeted test, then compile or broader gates as needed.
4. Update docs or feature metadata only when behavior changes.

Repository hardening:

1. Inspect `.github/workflows/*.yml`, `scripts/repo/*.sh`, `zai_coder/github_ready_core/*.py`, and relevant tests.
2. Keep safety checks narrow and regression-tested.
3. Verify exact blocked patterns: `git add .`, `git add -A`, `--no-verify`, force push, broad deletion, and pipe-to-shell.

Roadmap/release work:

1. Use `ROADMAP.md` as canonical.
2. Keep shipped/local/dry-run/external-go-live states distinct.
3. Update release artifacts only if the task explicitly asks for release artifact changes.

Web migration work:

1. Start with `web/src/lib/zai/migration-manifest.json`.
2. Keep `tests/test_web_surface.py` and `scripts/repo/web-migration-report.py` aligned with web ownership claims.
3. Do not hide external go-live blockers by changing presentation only.

## External Action Boundaries

Read-only network inspection is acceptable within the user's requested scope.

Require explicit approval before:

- Git push, PR merge, release creation, tag creation, publishing packages, or deployment.
- Posting to social/media systems.
- Modifying cloud, DNS, GitHub, payment, provider, or third-party resources.
- Running paid jobs or remote agents.
- Writing credentials or changing credential storage.

When approval is ambiguous, produce a local plan or draft artifact instead.

## Final Response Expectations For AI Agents

When you finish work:

- Name the files changed.
- State the validation commands run and their results.
- State any skipped gates or blockers.
- Do not bury production-readiness caveats.
- Keep the summary concrete and short.
