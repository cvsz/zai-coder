# Multi-Tenant Control Guide

## Commands

```bash
make multi-tenant-control
make tenant-status
make tenant-onboarding-plan
make tenant-demo-create
make tenant-demo-create APPLY=1
make tenant-api-key-plan
make tenant-api-key-plan APPLY=1
make tenant-isolation-check
make workspace-quota-check
make tenant-provider-permission PROVIDER=github
make tenant-backup-policy
make tenant-migration-plan
make tenant-dashboard-export
```

## Routes

```text
/api/tenants/status
/tenants
/tenants/onboarding
/tenants/backup
/tenants/migration
```
