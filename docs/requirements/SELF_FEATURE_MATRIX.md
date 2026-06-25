# ZAI Coder self-* Feature Matrix

Total features: **30**

| Feature | Category | Maturity | Mutation | Description |
|---|---|---|---:|---|
| `self-doctor` | diagnostics | ready | no | Run local health checks for Python, package files, config, Ollama, disk, and safe command policy. |
| `self-test` | quality | ready | no | Run unit tests and summarize failures without modifying source files. |
| `self-lint` | quality | planned | no | Run lightweight syntax and style checks with compileall and optional linters when installed. |
| `self-scan` | intelligence | ready | no | Scan project structure while ignoring generated and protected paths. |
| `self-index` | intelligence | next | no | Build a local file and symbol index for fast project navigation. |
| `self-rag` | intelligence | next | no | Build local retrieval context from project chunks and memory. |
| `self-plan` | orchestration | ready | no | Generate a safe implementation plan before edits. |
| `self-orchestrate` | orchestration | next | no | Coordinate planner, coder, reviewer, tester, security, and docs agents. |
| `self-queue` | orchestration | next | yes | Persist tasks with queued/running/completed/failed/cancelled states. |
| `self-heal` | repair | next | yes | Detect failed tests or broken commands, propose minimal patches, and require approval before apply. |
| `self-repair` | repair | next | yes | Apply verified patches through git apply after safety checks. |
| `self-review` | quality | ready | no | Review plans or diffs for risks, test coverage, and repo safety rules. |
| `self-audit` | governance | ready | no | Record and inspect audit events for agent, HTTP, patch, and command activity. |
| `self-govern` | governance | next | yes | Apply policy profiles for command allowlists, protected paths, and approval modes. |
| `self-secure` | security | ready | no | Scan commands and paths for secrets, bypass flags, broad deletes, and generated artifacts. |
| `self-redact` | security | next | no | Redact tokens, API keys, and private paths before model or log storage. |
| `self-backup` | resilience | ready | yes | Create local checkpoints before patch or risky mutations. |
| `self-rollback` | resilience | next | yes | Restore a previous checkpoint and audit the rollback. |
| `self-monitor` | observability | next | no | Monitor local CPU, RAM, disk, Ollama status, queue health, and recent failures. |
| `self-benchmark` | quality | next | no | Benchmark model latency, prompt quality, and safety-rule adherence. |
| `self-evaluate` | quality | next | no | Evaluate agents against regression prompts and expected safety outcomes. |
| `self-document` | docs | ready | yes | Generate or update requirement docs, feature matrix, and operator runbooks. |
| `self-explain` | docs | ready | no | Explain package capabilities, commands, and next roadmap. |
| `self-update` | maintenance | next | yes | Update package scaffolds through safe patch bundles, never curl-pipe shell. |
| `self-upgrade` | maintenance | next | yes | Apply versioned migrations for config, memory, and task queue schemas. |
| `self-host` | deployment | ready | yes | Run local API/web UI on localhost by default. |
| `self-deploy` | deployment | next | yes | Generate deploy plans for systemd, Docker, and reverse proxy without mutating production by default. |
| `self-package` | release | ready | yes | Build a release ZIP after tests and safety checks. |
| `self-clean` | maintenance | ready | yes | Remove only local Python/test cache files. |
| `self-media` | media | ready | yes | Generate local SVG/WAV/storyboard artifacts for image, voice, music, animation, and video planning. |
