# TUI Full Implementation Audit

Generated during the repository-aware TUI production-readiness pass.

## Files Inspected

- Root release and command files: `README.md`, `pyproject.toml`, `Makefile`, `run.sh`, `zai-coder`, `zai_coder/cli.py`.
- Installer and safety scripts: `scripts/safety-dry-run.sh`, `scripts/install/install-local-safe.sh`, `scripts/install/post-install-check.sh`, `scripts/install/uninstall-local-safe.sh`.
- TUI source: `zai_coder/tui/**/*.py`.
- TUI tests: `tests/test_tui_*.py`.
- TUI docs: `docs/tui/*.md`, `2026-06-26-tui-template-system-design.md`.
- Broader platform source/docs were scanned for incomplete indicators with the requested marker search.

## Detected Scaffold, Stub, Or Placeholder Items

- TUI config previously returned an untyped dictionary and did not expose `TuiConfig` or `resolve_tui_config`.
- TUI loader previously returned only names from `list_templates()` and lacked `TemplateInfo`, `get_template_info()`, numeric aliases, and class-level loading.
- TUI state previously persisted only a subset of required fields and lacked public `state_to_dict()`, `state_from_dict()`, `append_log()`, and `switch_template()` helpers.
- TUI action results previously lacked the requested `action_name`, `returncode`, `duration_ms`, and `reason` fields.
- TUI safety lacked a public `contains_secret_like_text()` helper and did not explicitly block external `curl`/`wget` URLs.
- TUI navigation lacked command palette metadata, help entries, and explicit template switch metadata.
- TUI docs were present but did not include the full implementation audit, installed launcher usage, troubleshooting, or release validation checklist.
- Broader platform scan found intentional older release-era "draft", "sandbox", and "scaffold" language in payment, connector, creative export, and historical requirements/docs. Those areas are outside the TUI implementation scope and remain local/draft-only by design.

## What Is Already Real

- Six TUI templates exist as concrete classes under `zai_coder/tui/templates/`.
- The CLI has a `tui` command with dry-run, config, template listing, and non-Textual preview paths.
- Textual is optional in `pyproject.toml`.
- The installer creates a launcher that prefers `python3 -m zai_coder "$@"`.
- The Makefile includes non-interactive TUI validation targets.
- The safety model is local-first and blocks external mutation by default.

## What Was Incomplete

- Typed config and typed template registry APIs.
- Complete alias handling for `01` through `06`.
- State conversion and redacted persistence helpers.
- Public navigation and command palette metadata.
- Complete action result shape and repo-pinned subprocess execution.
- Test coverage for invalid templates, missing Textual behavior, persistence failure, navigation, and allowlist metadata.
- Documentation depth for enterprise release validation and troubleshooting.

## Implementation Plan

- Keep Textual optional and lazy-loaded.
- Preserve existing CLI, installer, doctor, test, safety, and release behavior.
- Upgrade the TUI modules in place instead of introducing a separate framework.
- Add tests for all new public TUI contracts.
- Validate local install and installed launcher behavior.
- Stage only relevant TUI source/docs/tests and required launcher/installer files.

## Safety Risks

- Secret leakage through command output or persisted state: mitigated with redaction before display and save.
- External mutation from command palette actions: mitigated by a strict allowlist and blocklist.
- Accidental `APPLY=1`: blocked by TUI safety.
- Textual import failure breaking non-TUI CLI: mitigated by lazy imports and tested non-Textual paths.
- Runtime DB/evidence churn during tests: mitigated by restoring generated artifacts before staging.

## Validation Plan

```bash
python3 -m pytest -q
make test
make safety-check
make tui-check
./run.sh tui --dry-run
./run.sh tui --print-config
./run.sh tui --list-templates
./run.sh tui --template command-center --dry-run
./run.sh tui --template agent-hub --dry-run
./run.sh tui --template flow-stream --dry-run
./run.sh tui --template architect-tree --dry-run
./run.sh tui --template creative-canvas --dry-run
./run.sh tui --template operation-gate --dry-run
./run.sh tui --template operation-gate --no-textual
make install APPLY=1
make post-install-check
~/.local/bin/zai-coder doctor
~/.local/bin/zai-coder tui --dry-run
~/.local/bin/zai-coder tui --print-config
~/.local/bin/zai-coder tui --list-templates
~/.local/bin/zai-coder tui --template command-center --dry-run
~/.local/bin/zai-coder tui --template operation-gate --dry-run
```

## Final Acceptance Checklist

- All tests pass.
- `make tui-check` passes.
- Local install passes.
- Installed launcher supports TUI dry-run, config, list, and selected templates.
- All six templates are implemented and testable.
- Safety allowlist and blocklist work.
- Textual remains optional.
- No external deployment, release tag, GitHub Release, registry push, or service mutation is performed.
- Runtime DB/evidence/cache artifacts are not staged.
