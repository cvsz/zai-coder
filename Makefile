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
PACKAGE_NAME ?= zai-coder-final
SAFETY := ./scripts/safety-dry-run.sh --apply $(APPLY) --

.PHONY: help dry-run doctor install test compile safety-check scan ask chat serve run-command patch-check patch-apply package clean-preview clean-safe models status

help:
	@printf '%s\n' 'ZAI Coder Makefile targets:'
	@printf '%s\n' ''
	@printf '%s\n' '  make dry-run                Preview the default safe workflow'
	@printf '%s\n' '  make doctor                 Preview ./zai-coder doctor'
	@printf '%s\n' '  make test                   Preview pytest'
	@printf '%s\n' '  make scan                   Preview project scan'
	@printf '%s\n' '  make ask PROMPT="..."       Preview agent ask'
	@printf '%s\n' '  make run-command COMMAND="git status --short"'
	@printf '%s\n' '  make patch-check PATCH=fix.diff'
	@printf '%s\n' '  make patch-apply PATCH=fix.diff APPLY=1'
	@printf '%s\n' '  make serve APPLY=1          Start local web UI'
	@printf '%s\n' '  make install APPLY=1        Run installer'
	@printf '%s\n' '  make clean-safe APPLY=1     Remove only safe cache files'
	@printf '%s\n' '  make package APPLY=1        Build release ZIP'
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
	$(SAFETY) ./install.sh

test:
	$(SAFETY) $(PYTHON) -m pytest -q

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

clean-preview:
	@echo 'Safe cleanup preview:'
	@find . -type d \( -name __pycache__ -o -name .pytest_cache \) -print
	@find . -type f \( -name '*.pyc' -o -name '*.pyo' \) -print

clean-safe:
	@echo 'Cleaning only Python/test cache files. APPLY=$(APPLY)'
	@if [[ "$(APPLY)" != "1" ]]; then \
	  $(MAKE) --no-print-directory clean-preview; \
	  echo 'Set APPLY=1 to remove listed cache files.'; \
	else \
	  find . -type d -name __pycache__ -prune -exec rm -rf {} +; \
	  find . -type d -name .pytest_cache -prune -exec rm -rf {} +; \
	  find . -type f \( -name '*.pyc' -o -name '*.pyo' \) -delete; \
	  echo 'Safe cache cleanup complete.'; \
	fi
