# Evaluation and Benchmark System

ZAI Coder is packaged with an internalized regression and evaluation benchmarking tool suite (`evals`). This system tests the safety, redaction, task workflows, and index capabilities deterministically against pre-defined prompt payloads.

## Features
- **Offline Evaluation**: Relies on a local `Echo` simulated model mapping assertions, allowing regressions to be discovered without needing OpenAI/Ollama limits.
- **Suite Segmentation**: Separates tests cleanly into `safety`, `agents`, `rag`, `tool-runtime`, `model-router`, and `server`.
- **JSON Benchmarks**: Dumps full results into `.json` logs, designed for CI/CD tracking thresholds.

## CLI Usage

```bash
# List available eval suites
./zai-coder eval list

# Run a suite
./zai-coder eval run --suite safety

# Run benchmarking directly to JSON stdout
./zai-coder bench models
./zai-coder bench safety
```

## Structure
- `assets/evals/*.json` : JSON-serialized cases representing a single test input/output mapping limit.
- `zai_coder/evals/runner.py` : Invokes localized logic or dry-runs API layers simulating the inputs to ensure safety boundaries block malicious paths.
