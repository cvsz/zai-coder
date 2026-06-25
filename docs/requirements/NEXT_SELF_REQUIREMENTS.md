# ZAI Coder Next Requirements: all self-* systems

Target package: `zai-coder-control-plane-v2-self.zip`

## Goals

- Keep local-first operation as the default.
- Make every risky action dry-run-first.
- Add self-diagnostics, self-repair, self-monitoring, self-documentation, self-hosting, self-packaging, and self-governance.
- Preserve hard safety rules: no `git add .`, no `git add -A`, no `--no-verify`, no force push, no `apps/zlms/**`, no secrets, no generated artifacts.

## Baseline ready self-* features

- `self-doctor` — Run local health checks for Python, package files, config, Ollama, disk, and safe command policy.
- `self-test` — Run unit tests and summarize failures without modifying source files.
- `self-scan` — Scan project structure while ignoring generated and protected paths.
- `self-plan` — Generate a safe implementation plan before edits.
- `self-review` — Review plans or diffs for risks, test coverage, and repo safety rules.
- `self-audit` — Record and inspect audit events for agent, HTTP, patch, and command activity.
- `self-secure` — Scan commands and paths for secrets, bypass flags, broad deletes, and generated artifacts.
- `self-backup` — Create local checkpoints before patch or risky mutations.
- `self-document` — Generate or update requirement docs, feature matrix, and operator runbooks.
- `self-explain` — Explain package capabilities, commands, and next roadmap.
- `self-host` — Run local API/web UI on localhost by default.
- `self-package` — Build a release ZIP after tests and safety checks.
- `self-clean` — Remove only local Python/test cache files.
- `self-media` — Generate local SVG/WAV/storyboard artifacts for image, voice, music, animation, and video planning.

## Next implementation requirements

### deployment

- `self-deploy`
  - Requirement: Generate deploy plans for systemd, Docker, and reverse proxy without mutating production by default.
  - Commands: `./zai-coder deploy plan`
  - Outputs: deployment checklist
  - Safety: operator approval required

### governance

- `self-govern`
  - Requirement: Apply policy profiles for command allowlists, protected paths, and approval modes.
  - Commands: `./zai-coder policy check`
  - Outputs: policy decision
  - Safety: deny by default for high-risk actions

### intelligence

- `self-index`
  - Requirement: Build a local file and symbol index for fast project navigation.
  - Commands: `./zai-coder index build`
  - Outputs: SQLite file index, symbol table
  - Safety: no generated paths, no secrets indexing
- `self-rag`
  - Requirement: Build local retrieval context from project chunks and memory.
  - Commands: `./zai-coder rag build`, `./zai-coder ask --with-rag ...`
  - Outputs: chunk table, retrieval results
  - Safety: local-first, redact secrets before storing chunks

### maintenance

- `self-update`
  - Requirement: Update package scaffolds through safe patch bundles, never curl-pipe shell.
  - Commands: `./zai-coder update check`
  - Outputs: update plan, patch bundle
  - Safety: dry-run first, no auto-update from remote scripts
- `self-upgrade`
  - Requirement: Apply versioned migrations for config, memory, and task queue schemas.
  - Commands: `./zai-coder migrate`
  - Outputs: migration report
  - Safety: backup before migration

### observability

- `self-monitor`
  - Requirement: Monitor local CPU, RAM, disk, Ollama status, queue health, and recent failures.
  - Commands: `./zai-coder self monitor`
  - Outputs: health report
  - Safety: read-only

### orchestration

- `self-orchestrate`
  - Requirement: Coordinate planner, coder, reviewer, tester, security, and docs agents.
  - Commands: `./zai-coder task create --agent supervisor`
  - Outputs: task graph, agent logs
  - Safety: approval required before writes
- `self-queue`
  - Requirement: Persist tasks with queued/running/completed/failed/cancelled states.
  - Commands: `./zai-coder task list`, `./zai-coder task logs TASK_ID`
  - Outputs: SQLite queue, run logs
  - Safety: bounded workers, cancel support

### quality

- `self-lint`
  - Requirement: Run lightweight syntax and style checks with compileall and optional linters when installed.
  - Commands: `make compile`, `./zai-coder self runbook self-lint`
  - Outputs: lint report
  - Safety: read-only
- `self-benchmark`
  - Requirement: Benchmark model latency, prompt quality, and safety-rule adherence.
  - Commands: `./zai-coder bench models`
  - Outputs: benchmark report
  - Safety: small prompts by default
- `self-evaluate`
  - Requirement: Evaluate agents against regression prompts and expected safety outcomes.
  - Commands: `./zai-coder eval run`
  - Outputs: eval scores
  - Safety: no source mutation

### repair

- `self-heal`
  - Requirement: Detect failed tests or broken commands, propose minimal patches, and require approval before apply.
  - Commands: `./zai-coder self heal --check`
  - Outputs: fix plan, candidate patch
  - Safety: dry-run first, checkpoint before apply, no destructive commands
- `self-repair`
  - Requirement: Apply verified patches through git apply after safety checks.
  - Commands: `./zai-coder patch fix.diff --check`, `make patch-apply PATCH=fix.diff APPLY=1`
  - Outputs: checkpoint, audit entry
  - Safety: APPLY=1 required, patch check before apply

### resilience

- `self-rollback`
  - Requirement: Restore a previous checkpoint and audit the rollback.
  - Commands: `./zai-coder checkpoint restore CHECKPOINT_ID`
  - Outputs: restored files, audit entry
  - Safety: explicit checkpoint id, confirmation required

### security

- `self-redact`
  - Requirement: Redact tokens, API keys, and private paths before model or log storage.
  - Commands: `./zai-coder redact FILE`
  - Outputs: redacted text
  - Safety: never print raw secrets

## Acceptance checks

```bash
make doctor
make self-list
make self-plan
make self-requirement-next
make test
make safety-check
```

Expected: all tests pass, unsafe commands remain blocked, generated requirement docs contain every self-* feature.
