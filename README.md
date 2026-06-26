# ZAI Coder - Enterprise Control Plane

A local-first, python-standard-library-centric AI autonomous agent operations plane prioritizing secure offline execution without sacrificing automation.

## Core Pillars

- **Local First**: Safe offline command operation, deterministic text evaluation metrics.
- **Python Standard Library**: No mandatory third party web framework layers for internal execution logic.
- **Enterprise Safety Guards**: Action approvers requiring dry-run manual reviews, redaction filters for secrets, and dynamic execution profiles.
- **Hermes-Compatible Skills**: Marketplace manifests can model Hermes Agent `SKILL.md` workflows while preserving ZAI Coder policy gates.

## Architecture Highlights

- Fully transparent task queuing.
- Offline RAG chunking and lexical database indexing.
- Standalone deploy planner that never auto-mutates hosts.
- Embedded continuous observability metrics.
- Policy-gated Agent Marketplace with skill manifests, compatibility checks, install/enable approvals, and audit logs.
- No `git add .` allowed.

## Quick Start

```bash
make install-dry-run
./zai-coder self heal --check
make package APPLY=1
```

## Skills and Marketplace

ZAI Coder includes an Agent Marketplace layer for reusable local skills. Skills are tracked through `SkillManifest` records, can be searched by category/tags/source, and are designed to align with the Hermes Agent `SKILL.md` model:

```bash
make skill-catalog
make marketplace-search QUERY=hermes
make skill-install-policy SKILL_ID=hermes-skill-author AGENT_TYPE=builder
```

See:

- `docs/marketplace/AGENT_MARKETPLACE_AND_SKILLS_GUIDE.md`
- `docs/marketplace/SKILL_MANIFEST.md`
- `docs/marketplace/HERMES_SKILLS_ALIGNMENT.md`
- `skills/hermes-skill-author/SKILL.md`

Refer to the `docs/` folder for explicit CLI usage maps, system diagrams, and regression pipeline outlines.
