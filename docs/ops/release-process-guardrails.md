# Release Process Guardrails

## Purpose
Define a PR-first release workflow that prevents direct-main release confusion and protects signed tags, GitHub releases, package artifacts, and post-release verification records.

## Background
v0.1.3 was successfully released and validated, but release/publish verification work partially bypassed the intended publish branch. History is correct and must not be rewritten. These guardrails prevent recurrence.

## Release Branch Model
1. Planning PR
2. Feature/hardening PRs
3. Final readiness PR
4. Release candidate PR
5. Publish branch / publish phase
6. Post-release verification PR
7. Cleanup / hygiene PRs

## No Direct Main Release Rule
- Never commit release/publish/post-release docs directly to main.
- All release process changes must go through a PR unless emergency recovery is explicitly documented.
- Tags must be created only after main is verified at the intended release commit.
- Post-release verification docs must go through PR unless emergency recovery requires otherwise.

## Allowed Release Mutations
Only in publish phase:
- create signed tag
- push release tag
- create GitHub release
- upload release assets

## Disallowed Actions
- force push
- tag rewrite
- release asset replacement without recovery plan
- direct-main package version bump
- direct-main release verification commit
- committing dist artifacts
- committing runtime DB/evidence state

## Required Checks Before Tag
- clean working tree
- version matches target
- full tests pass
- repo-check passes
- secret-scan passes
- stage-manifest-check passes
- package-check passes
- generated-state guard passes
- CI dependency setup verified

## Required Checks After Publish
- tag verifies
- GitHub release exists
- all expected assets attached
- checksums pass
- post-release validation passes
- generated files remain untracked

## Emergency Recovery
If direct-main release work accidentally happens:
- do not rewrite history by default
- verify final release state
- document actual commit ledger
- create a follow-up guardrail or reconciliation PR
