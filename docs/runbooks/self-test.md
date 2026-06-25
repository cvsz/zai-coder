# Runbook: self-test

Run unit tests and summarize failures without modifying source files.

## Commands

```bash
make test
```
```bash
python3 -m pytest -q
```

## Outputs

- pytest report

## Safety

- dry-run by default through Makefile
