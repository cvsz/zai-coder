# Artifact Registry

The `artifact` command tracks local files that should be referenced by later work, reviews, or release gates.

## Commands

```bash
./zai-coder artifact add --path docs/ops/self-queue.md --label "Self Queue Runbook" --kind doc --tags self-queue,ops
./zai-coder artifact list
./zai-coder artifact show ARTIFACT_ID
./zai-coder artifact export --json
```

## Storage

- Registry DB: `.zai-coder/artifacts/artifacts.db`
- Export shape: schema version plus artifact records
- Record fields: path, label, kind, sha256, size, description, tags, created_at

## Safety

- Artifact paths must stay inside the workspace.
- Secret-like paths such as `.env`, token files, and secret files are blocked.
- The registry is local-only. It does not upload, publish, push, or open remote jobs.

