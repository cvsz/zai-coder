# Provider Routing

ZAI Coder uses a flexible `ProviderRouter` to select the best LLM provider based on task requirements and availability.

## Route Properties

- `provider_id`: Unique string ID (e.g., `openai-gpt4`).
- `provider_type`: Type of integration (e.g., `openai`, `anthropic`).
- `priority`: Integer sorting priority (lower is preferred).
- `enabled`: Toggle for active use.
- `requires_api_key`: If true, requires explicit environment variables.
- `supports_text`, `supports_vision`, `supports_audio`, `supports_tools`: Capability flags.
- `cost_tier`: Categorization (low, medium, high).

## Selection Logic

When executing a task, the router filters routes based on requirements (e.g., vision support) and selects the lowest-priority enabled route.
