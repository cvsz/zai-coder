# Agent Marketplace and Skills Guide

The Agent Marketplace is the local-first control plane for discovering, validating, installing, enabling, reviewing, exporting, and packing reusable agent skills. The current implementation is aligned with the Hermes Agent skills model while preserving ZAI Coder's enterprise defaults: policy gates, tenant scope, auditability, and dry-run-first execution.

## Commands

```bash
make agent-marketplace-and-skills
make marketplace-status
make skill-catalog
make marketplace-search QUERY=release
make marketplace-search QUERY=hermes
make skill-validate
make skill-compatibility AGENT_TYPE=builder SKILL_ID=repo-planner
make skill-install-policy SKILL_ID=repo-planner AGENT_TYPE=builder
make skill-install-policy SKILL_ID=hermes-skill-author AGENT_TYPE=builder
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

## Hermes Skills alignment

Hermes treats skills as on-demand `SKILL.md` instruction documents. A catalog exposes lightweight metadata first, then the full skill content loads only when the task matches. ZAI Coder mirrors that model with `SkillManifest.description`, `tags`, `category`, `platforms`, `source`, `source_slug`, `required_environment_variables`, and `hermes_metadata`.

Supported source values:

- `local`
- `bundled`
- `official`
- `skills-sh`
- `well-known`
- `github`
- `url`
- `clawhub`
- `lobehub`
- `browse-sh`

For hub and external sources, keep `source_slug` populated so installs are reproducible and auditable.

## Recommended flow

1. **Discover** with `make skill-catalog` or `make marketplace-search QUERY=<term>`.
2. **Inspect** the manifest, including source, platform filter, permissions, and Hermes metadata.
3. **Validate** with the manifest validator and security report.
4. **Check compatibility** against the requested agent type.
5. **Plan install** through `make skill-install-policy`.
6. **Install dry-run first**, then apply only after review.
7. **Enable after approval** when a skill is intended to run in active workflows.
8. **Audit and export** the marketplace state for release or team review.

## Skill authoring rules

Use this structure for new skill folders:

```text
skills/<category>/<skill-id>/
├── SKILL.md
├── references/
├── templates/
├── scripts/
└── assets/
```

A minimal `SKILL.md` should include:

```markdown
---
name: my-skill
description: Short description for catalog discovery.
version: 1.0.0
platforms: [linux, macos]
metadata:
  hermes:
    tags: [automation]
    category: devops
    requires_toolsets: [terminal]
---
# My Skill

## When to Use
State exact trigger conditions.

## Procedure
1. Describe safe, repeatable steps.

## Pitfalls
- List known failure modes.

## Verification
Describe how to confirm success.
```

## Enterprise guardrails

- Do not install directly into active workflows without dry-run output.
- Keep apply-level permissions (`providers:apply`, `execution:apply`) rare and manually approved.
- Treat external `url`, `github`, `well-known`, and community registry sources as supply-chain inputs.
- Preserve source provenance in `source_slug`.
- Keep secret values out of manifests; store only environment variable names.
- Prefer bundles or default skill plans for repeated workflows rather than loading broad skill catalogs into every prompt.
