# TUI Safety Model

The TUI is local-first and dry-run-first. Textual is optional, and non-TUI CLI commands do not import Textual.

## Allowed Command Registry

Only these local commands may be executed by TUI actions:

```text
./run.sh doctor
make safety-check
make final-release-status
make install-dry-run
./run.sh tui --print-config
```

## Blocked Commands

The TUI blocks:

- `git push`
- `gh release`
- `terraform apply`
- `kubectl apply`
- `docker push`
- `cloudflare`
- `stripe`
- Any command containing `APPLY=1`
- `curl` or `wget` to external URLs
- Commands containing obvious tokens, secrets, credentials, private keys, API keys, or passwords
- Arbitrary shell commands from user input

Dry-run previews do not execute subprocesses. Runtime output is redacted before display and before state persistence.

## Dry-Run-First Rules

- TUI actions may only execute the allowlisted local read/check commands.
- TUI actions never run `APPLY=1`.
- Approval in `operation-gate` records local dry-run evidence only.
- Release, deploy, publish, upload, registry push, and external-service mutation remain outside the TUI.
