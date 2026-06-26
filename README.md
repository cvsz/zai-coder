# ZAI Coder - Enterprise Control Plane
A local-first, python-standard-library-centric AI autonomous agent operations plane prioritizing secure offline execution without sacrificing automation.

## Core Pillars
- **Local First**: Safe offline command operation, deterministic text evaluation metrics.
- **Python Standard Library**: No mandatory third party web framework layers for internal execution logic.
- **Enterprise Safety Guards**: Action approvers requiring dry-run manual reviews, redaction filters for secrets, and dynamic execution profiles.

## Architecture Highlights
- Fully transparent task queuing.
- Offline RAG chunking and lexical database indexing.
- Standalone deploy planner that never auto-mutates hosts.
- Embedded continuous observability metrics.
- No `git add .` allowed.

## Quick Start
```bash
make install-dry-run
./zai-coder self heal --check
make package APPLY=1
```

Refer to the `docs/` folder for explicit CLI usage maps, system diagrams, and regression pipeline outlines.
