# Dry-run Updater

Update steps:

1. verify artifact checksum
2. create backup
3. stop schedulers
4. apply update package
5. run migrations in dry-run mode
6. run smoke tests
7. resume schedulers
8. write release audit event
