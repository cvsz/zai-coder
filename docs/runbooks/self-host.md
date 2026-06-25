# Runbook: self-host

Run local API/web UI on localhost by default.

## Commands

```bash
./zai-coder serve --host 127.0.0.1 --port 8765
```
```bash
make serve APPLY=1
```

## Outputs

- local web UI

## Safety

- localhost default
- remote bind requires auth in next phase
