# Safe Log Viewer

Only safe relative log paths are accepted:

```text
logs/*
data/*
```

Blocked examples:

```text
/etc/passwd
../secret
apps/zlms/*
.git/*
node_modules/*
```

Use:

```bash
make ops-log-viewer LOG_PATH=logs/zai-coder.log
```
