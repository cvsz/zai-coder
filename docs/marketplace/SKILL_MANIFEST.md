# Skill Manifest

ZAI Coder skill manifests are local-first records that map external or internal `SKILL.md` workflows into the Agent Marketplace. They are intentionally compatible with the Hermes Agent skill model while keeping ZAI Coder's policy gates, tenant audit trail, dry-run install flow, and manual enable approvals.

## Required fields

| Field | Purpose |
|---|---|
| `id` | Stable local skill id. Must be a safe slug without `/`, `\\`, or `..`. |
| `name` | Human-readable display name. |
| `version` | Skill package or manifest version. |
| `description` | Short progressive-disclosure summary. Keep this concise because agents read catalog descriptions before loading full skill content. |
| `entrypoint` | Markdown entrypoint, normally `SKILL.md`. |
| `required_permissions` | ZAI Coder permissions needed before install/enable. |
| `compatible_agent_types` | Agent types allowed to use the skill. |

## Hermes-aligned optional fields

| Field | Purpose |
|---|---|
| `category` | Catalog grouping such as `planning`, `release`, `infrastructure`, `skills`, or `billing`. |
| `tags` | Searchable tags. These mirror `metadata.hermes.tags` when imported from Hermes-style frontmatter. |
| `platforms` | Optional platform filter: `linux`, `macos`, and/or `windows`. Empty means all platforms. |
| `source` | Skill origin: `local`, `bundled`, `official`, `skills-sh`, `well-known`, `github`, `url`, `clawhub`, `lobehub`, or `browse-sh`. |
| `source_slug` | Audit slug for hub/external sources, for example `openai/skills/k8s`, `official/security/1password`, or `well-known:https://example.com/.well-known/skills/acme`. |
| `required_environment_variables` | Secret/config prerequisites declared by the skill. Values are tracked as names only. |
| `hermes_metadata` | Raw Hermes metadata extracted from `metadata.hermes`, including `category`, `tags`, `requires_toolsets`, `fallback_for_toolsets`, `requires_tools`, `fallback_for_tools`, and `config`. |

## Compatible SKILL.md frontmatter

```markdown
---
name: hermes-skill-author
description: Authors Hermes-compatible SKILL.md workflows.
version: 1.0.0
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [hermes, skills, skill.md]
    category: skills
    requires_toolsets: [terminal]
---
# Hermes Skill Author

## When to Use
Use this when you need a reusable Hermes Agent skill.

## Procedure
1. Keep the description short for progressive disclosure.
2. Use standard sections: When to Use, Procedure, Pitfalls, Verification.
3. Add supporting files under references/, templates/, scripts/, or assets/ only when needed.

## Pitfalls
- Do not invent commands that the target project does not expose.
- Do not request apply-level permissions unless the workflow truly mutates state.

## Verification
Confirm the skill is discoverable and loads only when relevant.
```

## Validation rules

- Entrypoints must be Markdown files and must not escape the skill directory.
- Descriptions should stay short because they are used in progressive disclosure indexes.
- Hub or external sources must retain `source_slug` for auditability and upstream update checks.
- Platform filters are limited to `linux`, `macos`, and `windows`.
- Apply-level permissions such as `providers:apply` and `execution:apply` are flagged by the security report.
- Sensitive categories such as infrastructure and billing must declare explicit permissions.

## Install posture

ZAI Coder keeps install and enable as separate steps:

1. Import or author the manifest.
2. Validate manifest shape and Hermes metadata.
3. Run security report and compatibility checks.
4. Require dry-run install before install.
5. Require manual approval before enable when the skill can affect state.
6. Record install, enable, review, import/export, and pack-builder actions in the marketplace audit log.
