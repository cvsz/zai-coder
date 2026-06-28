# Evaluation and Benchmark System

ZAI Coder ships a deterministic local evaluation suite for the real agent, command-safety, and retrieval paths.

## Features
- **Planner contract evals**: The standalone `evals/run_local.py` harness executes the real `planner` agent prompt path and grades the output against exact contract rules.
- **Safety evals**: The package runner executes `ToolRuntime` with real safety and redaction checks.
- **Retrieval evals**: The package runner executes `LocalRAG` against the workspace index.
- **JSON reports**: Results are written as structured JSON for CI/CD tracking and regression diffs.

## CLI Usage

```bash
# List available eval suites
./zai-coder eval list

# Run a suite
./zai-coder eval run --suite agents

# Run benchmarking directly to JSON stdout
./zai-coder bench agents
./zai-coder bench safety
```

## Standalone Harness

```bash
python3 evals/run_local.py --suite planner-contract
```

The harness writes `evals/results/latest.json` and exits non-zero if any case fails.

## Structure
- `assets/evals/*.json` : Workspace-managed suites for command safety, agent prompt contracts, and retrieval checks.
- `evals/cases.jsonl` : Standalone planner-contract cases for the local harness.
- `zai_coder/evals/runner.py` : Executes the real local path for each suite kind and grades the result.
