# Release self-dev cleanup

This note documents the local cleanup workflow used before release-oriented ZAI Coder self-development.

## Why

Release and self-development workflows should not be blocked by local-only artifacts such as repo-local virtual environments, extracted ZIP bundles, local release directories, runtime SQLite databases, or generated logs.

The repository keeps tracked release documentation and source files under version control, but local generated artifacts must stay untracked.

## Safe workflow

```bash
cd /home/zeazdev/zai-coder

scripts/zai-self-dev.sh doctor
scripts/zai-self-dev.sh prompt
```

`plan` is intentionally offline and prints prompts only. Use `agent-plan` only when the configured model provider is known to be running.

```bash
scripts/zai-self-dev.sh agent-plan
```

## Clean worktree before sync

```bash
git status --short
```

If tracked files appear as deleted, restore only the exact files you did not intend to delete:

```bash
git restore PATH
```

Move local generated artifacts outside the repository:

```bash
mkdir -p /tmp/zai-coder-local-artifacts
mv zai-coder-self-dev-kit.zip /tmp/zai-coder-local-artifacts/ 2>/dev/null || true
mv zai-coder-self-dev-kit /tmp/zai-coder-local-artifacts/ 2>/dev/null || true
mv release /tmp/zai-coder-local-artifacts/ 2>/dev/null || true
```

Use local excludes for machine-only state:

```bash
APPLY=1 scripts/zai-self-dev.sh local-exclude
```

## Sync after clean

```bash
scripts/zai-self-dev.sh sync
```

## Release safety

Do not create tags, GitHub releases, or release assets from this automation kit. Publishing remains limited to the dedicated release phase and existing release docs/scripts.
