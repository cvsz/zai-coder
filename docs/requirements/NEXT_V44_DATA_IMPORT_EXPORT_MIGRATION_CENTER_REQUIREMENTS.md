# ZAI Coder Control Plane v44 — Data Import Export and Migration Center Requirements

## Added in v44

- Data source catalog.
- Import planning.
- Export planning.
- Migration job registry.
- Schema compatibility checks.
- Data mapping catalog.
- Rollback preview plans.
- Migration evidence exports.
- Migration dashboard routes.
- Migration center scripts/routes/docs/tests.

## Safety

- Dry-run migration planning by default.
- No direct data modification by default.
- No production database access by default.
- Rollback previews only.
- Demo/export writes require `APPLY=1`.
