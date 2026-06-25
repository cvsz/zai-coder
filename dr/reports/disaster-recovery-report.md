# Backup Restore and Disaster Recovery Report

## Backup Plans

- Configuration backup plan [daily / retention=14d / dry_run=True]
- Local SQLite backup plan [daily / retention=7d / dry_run=True]
- Evidence export backup plan [weekly / retention=30d / dry_run=True]

## Recovery Targets

- control-plane: RPO=15m RTO=60m [critical]
- developer-docs: RPO=240m RTO=480m [normal]
- evidence-exports: RPO=60m RTO=240m [high]

## Safety

- Restore workflows are preview-only by default.
- No direct production restore.
- Evidence export is local-only.
