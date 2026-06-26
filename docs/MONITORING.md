# Monitoring and Metrics

ZAI Coder supports fully localized observability. Telemetry checks are processed safely and synchronously via the `SystemMonitor` logic with deterministic snapshot metrics.

## Supported Checks
- **Python Version**: Core interpreter compatibility.
- **Platform**: Operating System details.
- **Disk Usage**: Identifies if index or artifact capacity limits hit thresholds.
- **Ollama**: Availability checks ping `localhost:11434` without relying on HTTP libraries (only using `socket`).
- **Database Health**: Scans `.zai-coder/tasks/tasks.db` and `.zai-coder/index/project-index.db` using read-only validations.
- **Audit Logs**: Monitors `.zai-coder/data/zai-audit.jsonl` size.
- **Config & Package**: Safe validations against dependencies and `config.json`.
- **Failures**: Mock baseline tracking for recent compilation or testing halts.

## Output Details

Zero external dependencies are necessary. The CLI strictly emits `JSON` structures for CI/CD metrics, or `Markdown` tables for human legibility.

```bash
# General health overview via tabular markdown
./zai-coder self monitor

# Complete programmatic json dump for metrics
./zai-coder metrics snapshot --json
```

## Security Posture
Metrics extraction reads metadata and system statuses. **Secrets** and explicit codebase contexts are deliberately blocked from metrics objects preserving local-first privacy defaults.
