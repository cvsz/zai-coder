# Hermes Skills Alignment

This note records how `cvsz/zai-coder` maps the Hermes Agent skills model into the local Agent Marketplace.

## Source facts

Hermes Agent documents skills as on-demand `SKILL.md` instruction packages. A short metadata index is read first, and the full skill is loaded only when needed. Hermes stores skills under `~/.hermes/skills/`, supports external skill directories, accepts frontmatter fields such as `name`, `description`, `version`, `platforms`, and `metadata.hermes`, and can browse/install from multiple sources including official optional skills, `skills.sh`, well-known endpoints, direct GitHub paths, and direct URLs.

## ZAI Coder mapping

| Hermes concept | ZAI Coder field or control |
|---|---|
| `SKILL.md` entrypoint | `SkillManifest.entrypoint` |
| Frontmatter `name` | `SkillManifest.name` and safe local `id` |
| Frontmatter `description` | `SkillManifest.description` |
| Frontmatter `version` | `SkillManifest.version` |
| Frontmatter `platforms` | `SkillManifest.platforms` |
| `metadata.hermes.tags` | `SkillManifest.tags` |
| `metadata.hermes.category` | `SkillManifest.category` |
| Conditional activation metadata | `SkillManifest.hermes_metadata` |
| Hub source slug | `SkillManifest.source` + `source_slug` |
| Required setup env vars | `SkillManifest.required_environment_variables` |
| Install security scan | `manifest_security_report()` |
| Install/enable gating | `install_policy_decision()` and `enable_policy_decision()` |
| Team export/reuse | Marketplace import/export and skill pack builder |

## Implementation posture

ZAI Coder does not blindly mirror a public hub into active workflows. It keeps skills observable and controlled:

1. Import metadata into a local manifest.
2. Validate shape, platform filters, source provenance, and entrypoint safety.
3. Run the security report.
4. Check agent compatibility and role permissions.
5. Require dry-run install.
6. Require approval before enable.
7. Audit every marketplace action.

## Recommended next implementation step

Add a `zai-coder marketplace import-skill <path-or-url>` command that reads Hermes-style `SKILL.md` frontmatter, converts it into `SkillManifest`, runs the validator/security report, and stores it as a disabled local install pending approval.
