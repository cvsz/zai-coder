# ZAI Coder Control Plane v3 — Growth Core Requirements

## Scope

Add five core product systems:

1. Members System
2. Update System
3. Core System
4. Marketing Shared
5. Social Media Core

## Members System

### Requirements

- Local SQLite-backed members table.
- Roles: owner, admin, developer, marketer, viewer.
- Permission checks via role grants.
- Invite records stored locally.
- No automatic external email send.
- Web/API integration later.
- Audit every member mutation.
- Never store plaintext passwords in this module.

### Future CLI

```bash
./zai-coder members list
./zai-coder members add --email user@example.com --role developer
./zai-coder members invite --email user@example.com --role marketer
./zai-coder members can --email user@example.com --permission social:write
```

## Update System

### Requirements

- Update manifest.
- Dry-run update plan.
- Safe path validation.
- Block absolute paths.
- Block parent traversal.
- Block apps/zlms/**.
- Block .env, node_modules, dist, .next, coverage, reports.
- Require checkpoint before apply.
- Require APPLY=1 for mutations.

### Future CLI

```bash
./zai-coder update check
./zai-coder update plan
./zai-coder update apply --manifest update.json
```

## Core System

### Requirements

- Feature registry.
- Health checks.
- Addon registry.
- Capability discovery.
- System status endpoint.
- Version manifest.
- Policy hooks.

## Marketing Shared

### Requirements

- Campaign model.
- Shared asset manifest.
- Content calendar.
- Channel planning.
- Reusable content snippets.
- Brand kit references.
- Approval workflow later.
- No external posting.

## Social Media Core

### Requirements

- Platform constraints.
- Post composer.
- Per-platform variant generator.
- Dry-run scheduler.
- Local scheduled post database.
- Approval status.
- External adapters later with explicit credentials.

## Safety

- Dry-run first.
- APPLY=1 required for mutations.
- No automatic social posting.
- No secret commits.
- No apps/zlms/**.
- No generated artifacts in package.
