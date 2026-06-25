# ZAI Coder Control Plane v45 — Backup Restore and Disaster Recovery Requirements

## Added in v45

- Backup plan registry.
- Restore drill preview runner.
- RPO/RTO target catalog.
- Disaster recovery scenario library.
- Recovery evidence reports.
- Backup validation checks.
- Restore readiness gate.
- DR dashboard routes.
- Disaster recovery scripts/routes/docs/tests.

## Safety

- Restore workflows are preview-only by default.
- No direct production restore by default.
- Evidence export is local-only.
- Manual approval required for real operations.
- Demo/export writes require `APPLY=1`.
