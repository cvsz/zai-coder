# OpenAI-Compatible API Plan

To facilitate integration with third-party tools, chat interfaces, and IDE extensions, ZAI Coder plans to implement a subset of the OpenAI API specification.

## Planned Endpoints

- `GET /v1/models`: List available local and configured agent models.
- `POST /v1/chat/completions`: The primary driver for interacting with ZAI Coder agents using standard Chat ML.
- `POST /v1/responses` (Optional/Later): Support for streaming and advanced object responses.

## Compatibility Guardrails

- We **do not** claim full OpenAI compatibility. We only claim compatibility for the specific endpoints implemented.
- These endpoints will run through the same `SafetyPolicy` and auditing pipeline as the CLI and TUI.
