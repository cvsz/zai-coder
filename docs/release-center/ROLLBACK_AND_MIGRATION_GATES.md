# Rollback and Migration Gates

Rollback requires:

- backup ready
- rollback manifest ready
- smoke tests defined

Migrations must use dry-run SQL and verify tenant scope when touching tenant data.
