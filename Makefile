SHELL := /usr/bin/env bash
.DEFAULT_GOAL := help

PYTHON ?= python3
APPLY ?= 0
HOST ?= 127.0.0.1
PORT ?= 8765
AGENT ?= coder
PROMPT ?= Inspect this repo and produce a safe fix plan.
COMMAND ?= git status --short
PATCH ?=
PACKAGE_NAME ?= zai-coder-clean-release
SAFETY := ./scripts/safety-dry-run.sh --apply $(APPLY) --

.PHONY: help dry-run doctor install install-dry-run uninstall post-install-check test compile safety-check scan ask chat serve run-command patch-check patch-apply package clean-preview clean-safe models status final-release-status tui tui-dry-run tui-check tui-command-center tui-agent-hub tui-flow-stream tui-architect-tree tui-creative-canvas tui-operation-gate gpg-commit gpg-push gpg-tag gpg-doctor gpg-list-keys gpg-loopback

help:
	@printf '%s\n' 'ZAI Coder Makefile targets:'
	@printf '%s\n' ''
	@printf '%s\n' '  make dry-run                Preview the default safe workflow'
	@printf '%s\n' '  make doctor                 Run ZAI Coder doctor'
	@printf '%s\n' '  make install APPLY=1        Install to PREFIX'
	@printf '%s\n' '  make install-dry-run        Preview install'
	@printf '%s\n' '  make uninstall APPLY=1      Uninstall from PREFIX'
	@printf '%s\n' '  make post-install-check     Verify installation'
	@printf '%s\n' '  make test                   Preview pytest'
	@printf '%s\n' '  make scan                   Preview project scan'
	@printf '%s\n' '  make ask PROMPT="..."       Preview agent ask'
	@printf '%s\n' '  make run-command COMMAND="git status --short"'
	@printf '%s\n' '  make patch-check PATCH=fix.diff'
	@printf '%s\n' '  make patch-apply PATCH=fix.diff APPLY=1'
	@printf '%s\n' '  make serve APPLY=1          Start local web UI'
	@printf '%s\n' '  make clean-safe APPLY=1     Remove only safe cache files'
	@printf '%s\n' '  make package APPLY=1        Build clean release TGZ + SHA256'
	@printf '%s\n' '  make final-release-status   Preview final release status'
	@printf '%s\n' '  make tui                    Launch optional Textual TUI'
	@printf '%s\n' '  make tui-check              Validate all TUI dry-run routes'
	@printf '%s\n' '  make gpg-commit             Safe GPG signed commit (APPLY=1)'
	@printf '%s\n' '  make gpg-push               Safe GPG signed push'
	@printf '%s\n' '  make gpg-tag                Safe GPG signed tag (APPLY=1)'
	@printf '%s\n' '  make gpg-doctor             GPG setup doctor'
	@printf '%s\n' '  make gpg-list-keys          List GPG keys'
	@printf '%s\n' '  make gpg-loopback           GPG loopback check'
	@printf '%s\n' ''
	@printf '%s\n' 'Safety: APPLY defaults to 0. Commands are printed, not executed, until APPLY=1.'
	@printf '%s\n' 'Blocked: git add ., git add -A, --no-verify, force push, broad rm -rf, apps/zlms/**, secrets/generated artifacts.'

dry-run:
	@$(MAKE) --no-print-directory status
	@$(MAKE) --no-print-directory safety-check
	@$(MAKE) --no-print-directory doctor
	@$(MAKE) --no-print-directory test

status:
	@echo '== status =='
	@pwd
	@find . -maxdepth 2 -type f | sort | head -80

doctor:
	$(SAFETY) ./zai-coder doctor

install:
	$(SAFETY) ./scripts/install/install-local-safe.sh

install-dry-run:
	./scripts/install/install-local-safe.sh

uninstall:
	$(SAFETY) ./scripts/install/uninstall-local-safe.sh

post-install-check:
	./scripts/install/post-install-check.sh

test:
	$(SAFETY) PYTHONPATH=. $(PYTHON) -m pytest -q --import-mode=importlib

compile:
	$(SAFETY) $(PYTHON) -m compileall -q zai_coder

safety-check:
	$(SAFETY) ./scripts/safety-check.sh .

scan:
	$(SAFETY) ./zai-coder scan

ask:
	$(SAFETY) ./zai-coder ask "$(PROMPT)" --agent "$(AGENT)"

chat:
	$(SAFETY) ./zai-coder chat --agent "$(AGENT)"

serve:
	$(SAFETY) ./zai-coder serve --host "$(HOST)" --port "$(PORT)"

run-command:
	$(SAFETY) ./zai-coder run "$(COMMAND)"

patch-check:
	@test -n "$(PATCH)" || (echo 'PATCH is required: make patch-check PATCH=fix.diff' >&2; exit 2)
	$(SAFETY) ./zai-coder patch "$(PATCH)" --check

patch-apply:
	@test -n "$(PATCH)" || (echo 'PATCH is required: make patch-apply PATCH=fix.diff APPLY=1' >&2; exit 2)
	@$(MAKE) --no-print-directory patch-check PATCH="$(PATCH)" APPLY=1
	$(SAFETY) ./zai-coder patch "$(PATCH)"

models:
	$(SAFETY) ./scripts/create_ollama_models.sh

package:
	$(SAFETY) ./scripts/package.sh "$(PACKAGE_NAME)"

final-release-status:
	$(SAFETY) ./scripts/final-release/final-release-status.sh

tui:
	./run.sh tui

tui-dry-run:
	./run.sh tui --dry-run

tui-check:
	./run.sh tui --print-config
	./run.sh tui --list-templates
	./run.sh tui --template command-center --dry-run
	./run.sh tui --template agent-hub --dry-run
	./run.sh tui --template flow-stream --dry-run
	./run.sh tui --template architect-tree --dry-run
	./run.sh tui --template creative-canvas --dry-run
	./run.sh tui --template operation-gate --dry-run

tui-command-center:
	./run.sh tui --template command-center --dry-run

tui-agent-hub:
	./run.sh tui --template agent-hub --dry-run

tui-flow-stream:
	./run.sh tui --template flow-stream --dry-run

tui-architect-tree:
	./run.sh tui --template architect-tree --dry-run

tui-creative-canvas:
	./run.sh tui --template creative-canvas --dry-run

tui-operation-gate:
	./run.sh tui --template operation-gate --dry-run

clean-preview:
	@echo 'Safe cleanup preview:'
	@find . -type d \( -name __pycache__ -o -name .pytest_cache \) -print
	@find . -type f \( -name '*.pyc' -o -name '*.pyo' \) -print

clean-safe:
	@echo 'Cleaning only Python/test cache files. APPLY=$(APPLY)'
	@if [[ "$(APPLY)" != "1" ]]; then 	  $(MAKE) --no-print-directory clean-preview; 	  echo 'Set APPLY=1 to remove listed cache files.'; 	else 	  find . -type d -name __pycache__ -prune -exec rm -rf {} +; 	  find . -type d -name .pytest_cache -prune -exec rm -rf {} +; 	  find . -type f \( -name '*.pyc' -o -name '*.pyo' \) -delete; 	  echo 'Safe cache cleanup complete.'; 	fi

gpg-commit:
	$(SAFETY) ./scripts/git/gpg-commit-safe.sh "$(COMMIT_MSG)"

gpg-push:
	@echo 'Manual-only: review git diff and run an explicit git push command outside this Makefile if approved.'
	@exit 2

gpg-tag:
	$(SAFETY) ./scripts/git/gpg-tag-safe.sh "$(TAG_NAME)"

gpg-doctor:
	$(SAFETY) ./scripts/git/gpg-doctor.sh

gpg-list-keys:
	$(SAFETY) ./scripts/git/gpg-list-keys.sh

gpg-loopback:
	$(SAFETY) ./scripts/git/gpg-loopback.sh
