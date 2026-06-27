# Automated Agent Runners Master Plan

## Purpose
This document establishes the architecture and phased rollout plan for fully automated, autonomous agent runners in ZAI Coder v0.1.4+.

## Current Baseline
ZAI Coder currently executes tasks interactively or via single-shot API calls. Operations run through a `SafetyPolicy` and generate `AuditLog` entries.

## Current Available Capabilities
- Single-shot execution via `run_server` / CLI
- `SafetyPolicy` path constraint checking
- `MemoryStore` / `LocalRAG` experimental capabilities
- `PatchRuntime` for file modifications
- `ModelRouter` for multi-provider fallback
- Experimental queue system (`SelfQueue`)

## Hermes-Style Feature Alignment
Features align strictly with deterministic, auditable, and safe execution bounds.

## Feature Statuses
- **available**: Core safety, memory primitives, manual toolsets.
- **partial**: Checkpoint/rollback, basic provider routing.
- **planned**: Subagent delegation, automated background runner, scheduling.
- **requires_integration**: MCP adapters, Provider-specific plugins.
- **do_not_claim**: Full OpenAI API, unconstrained background execution.

## Runner Architecture
The Agent Runner wraps tasks in deterministic boundaries (timeout, max steps, toolset). It operates synchronously by default, relying on local queues (e.g., `SelfQueue`) for offline scheduling.

## Agent Runner Lifecycle
1. Task enqueued with explicit bounds.
2. Runner dequeues, sets up workspace sandbox.
3. Execution proceeds iteratively.
4. Intermediate checkpoints saved.
5. Runner concludes (completed/failed/timeout) and produces a final summary.

## Toolset Model
Toolsets are explicitly defined groups of safe tools.

## Safe Execution Model
All commands route through `SafetyPolicy`; network requests are logged, paths are contained.

## Memory Model
LocalRAG/MemoryStore provides context isolation across tasks.

## Context Model
Explicit reference injection (`@file`) to prevent unintended context bloating.

## Checkpoint and Rollback Model
Iterative state saving during task loops to enable granular rollback.

## Scheduler Model
Local cron-based trigger mechanism for runners, disabled by default.

## Delegation Model
Hierarchical task assignment (Planner -> Coder -> Reviewer) with bounded subagent trees.

## Plugin and MCP Model
Opt-in registries for external capabilities, strongly filtered.

## Provider Routing Model
Fallback support across local and remote providers.

## Product Tiers and Claim-Control Model
Tiered feature flags to segregate experimental vs stable behaviors.

## Recommended PR Sequence
Refer to `AUTOMATED_AGENT_RUNNERS_PR_SEQUENCE.md`.

## Validation Gates
Strict unit/integration tests must pass before merging any phase.

## Explicit Non-Goals
- Resident daemons without explicit user consent.
- Unconstrained autonomous loops.
- Bypassing the local file sandbox.
