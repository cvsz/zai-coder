# Subagent Delegation

ZAI Coder supports safe hierarchical task delegation through the `DelegationOrchestrator`.

## Delegation Guardrails

To prevent run-away agent loops and state corruption, subagent delegation adheres strictly to these boundaries:

1. **Max Subagents**: Defaults to a maximum of 3 concurrent or sequential children per delegation plan.
2. **Isolated Context**: Each child receives an isolated workspace context.
3. **Restricted Toolset**: Subagents operate under a constrained `safe_runner_restricted` toolset profile to limit scope.
4. **No Shared Mutable State**: Children cannot directly mutate the parent's memory space or active references.
5. **Redacted Injection**: The parent collects only summaries of the child's work, which are explicitly tagged (e.g., `[REDACTED_FOR_PARENT]`) to prevent prompt-injection style attacks propagating from child output to parent logic.
