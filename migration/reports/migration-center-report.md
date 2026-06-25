# Data Import Export and Migration Center Report

## Jobs

- Import customer JSON plan [import_plan / review / dry_run=True]
- Export usage analytics plan [export_plan / draft / dry_run=True]
- Customer schema compatibility check [schema_check / review / dry_run=True]
- Rollback preview for customer import [rollback_preview / draft / dry_run=True]

## Safety

- Dry-run migration planning by default.
- No direct production database access.
- Rollback previews only.
