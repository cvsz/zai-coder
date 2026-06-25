# Backup Policy

## Default

```text
schedule: daily
retention: 14 days
include: data/, logs/, storage/
exclude: release/, node_modules/, .git/, apps/zlms/
encryption required: yes
restore test required: yes
```

## Commands

```bash
make production-backup-policy
make backup-plan
make backup-create APPLY=1
```
