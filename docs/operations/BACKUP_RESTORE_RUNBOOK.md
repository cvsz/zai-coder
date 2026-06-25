# Backup and Restore Runbook

## Backup

```bash
make backup-plan
make backup-create APPLY=1
```

## Restore

```bash
make restore-plan ARCHIVE=backups/zai-coder-control-plane-backup.tar.gz
make restore-apply APPLY=1 ARCHIVE=backups/zai-coder-control-plane-backup.tar.gz
```

## Safety

Inspect archive before extraction and run healthcheck after restore.
