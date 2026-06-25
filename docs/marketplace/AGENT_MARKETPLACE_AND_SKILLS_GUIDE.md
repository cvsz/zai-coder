# Agent Marketplace and Skills Guide

## Commands

```bash
make agent-marketplace-and-skills
make marketplace-status
make skill-catalog
make marketplace-search QUERY=release
make skill-validate
make skill-compatibility AGENT_TYPE=builder SKILL_ID=repo-planner
make skill-install-policy SKILL_ID=repo-planner AGENT_TYPE=builder
make skill-install-demo APPLY=1
make skill-enable-demo APPLY=1
make marketplace-audit
make skill-review-demo APPLY=1
make marketplace-export
make skill-pack-build
make skill-pack-build APPLY=1
make marketplace-dashboard-export
```

## Routes

```text
/api/marketplace/status
/marketplace
/marketplace/skills
/marketplace/agents
/marketplace/policy
```
