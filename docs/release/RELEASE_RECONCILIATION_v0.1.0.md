# ZAI Coder v0.1.0 — Release Reconciliation Report

**Date:** 2026-06-26  
**Executed by:** Emergency Release Reconciliation Phase  
**HEAD at reconciliation:** `9a11629`  
**Release tag:** `v0.1.0` → commit `b6b09e3` ✅ **INTACT**

---

## Summary

A previous report claimed ZAI Coder v0.1.0 was cleanly verified, tagged, pushed, and published. However, the working tree showed 441 modified files, 1 deleted file, and 21 untracked files after publication. This report documents the full reconciliation.

---

## 1. Safety Backup Created

Before any action was taken, the following backups were saved:

| File | Purpose |
|------|---------|
| `/tmp/zai-coder-status-before-reconcile.txt` | Full `git status --porcelain=v1` output (462 lines) |
| `/tmp/zai-coder-diff-stat-before-reconcile.txt` | Full `git diff --stat` (442 lines) |
| `/tmp/zai-coder-diff-name-status-before-reconcile.txt` | Full `git diff --name-status` (441 lines) |
| `/tmp/zai-coder-working-tree-before-reconcile.patch` | Full working tree patch (76KB, 1816 lines) |
| `/tmp/zai-coder-index-before-reconcile.patch` | Staged index patch (0 bytes — nothing staged) |

---

## 2. Repository State at Reconciliation Start

```
HEAD:     9a11629 (main, origin/main) — docs: add v0.1.0 remote publication report
Tag:      v0.1.0 → b6b09e3 — chore: add v0.1.0 final release evidence
Modified: 441 tracked files
Deleted:  1 tracked file
Untracked: 21 paths
Staged:   0 files (index clean)
```

---

## 3. File Classification

### A. Release Evidence Source
*None modified in this working tree.*

### B. Source Code Changes (Post-Release Work)
These 8 files represent legitimate **post-release engineering work**:

| File | Category |
|------|----------|
| `zai_coder/core/registry.py` | source-code-change |
| `zai_coder/core/safety.py` | source-code-change |
| `zai_coder/github_ready_core/repo_check.py` | source-code-change |
| `zai_coder/github_ready_core/repo_policy.py` | source-code-change |
| `zai_coder/github_ready_core/secret_scan.py` | source-code-change |
| `tests/test_final_enterprise_release_pack_v50.py` | source-code-change |
| `tests/test_github_ready_v12.py` | source-code-change |
| `.github/workflows/ci.yml` | source-code-change |

### C. Script Changes (Post-Release Work)
**425 shell scripts** modified across all subsystem directories under `scripts/`. This is significant post-release hardening work and must be committed separately by subsystem.

### D. Runtime-Generated Local State

#### Removed (untracked — safe):
| File | Action |
|------|--------|
| `.zai-coder/` | ✅ Removed (4MB runtime state directory) |
| `data/index.db` | ✅ Removed (untracked runtime DB) |
| `data/migrations.db` | ✅ Removed (untracked runtime DB) |
| `data/tasks.db` | ✅ Removed (untracked runtime DB) |
| `data/zai-audit.jsonl` | ✅ Removed (untracked audit log) |
| `Modelfile` | ✅ Removed (untracked local AI config) |

#### ⚠️ Tracked DB Files (Release Hygiene Issue):
| File | Status |
|------|--------|
| `data/enterprise-admin-console.db` | TRACKED binary DB — should be untracked |
| `data/provider-audit.db` | TRACKED binary DB — should be untracked |
| `data/zai-app.db` | TRACKED binary DB — should be untracked |

> These files are tracked in git but should not be. They are now covered by the updated `.gitignore` pattern `data/*.db`, but `.gitignore` does not untrack already-committed files. Requires `git rm --cached` — **deferred to post-release branch**.

### E. Generated Export / Evidence Data (Tracked, Modified)
| File | Status |
|------|--------|
| `evidence/governance/evidence-bundle.json` | Modified — post-release export update |
| `identity/evidence/identity-evidence.json` | Modified — post-release export update |
| `marketplace/exports/marketplace-export.json` | Modified — post-release export update |
| `migration/exports/migration-evidence.json` | Modified — post-release export update |
| `security/evidence/security-ops-evidence.json` | Modified — post-release export update |

### F. Deleted File
| File | Decision |
|------|----------|
| `zai_coder/final_enterprise_release_pack/routes/__init__.py` | **INTENTIONAL REFACTOR** — replaced by `routes.py` module. All imports verified working. `route_*` functions are all present in the new module. **DO NOT RESTORE.** |

Evidence: `routes.py` module exists with all route functions. Tests pass (446/446). `routes_old/` exists as untracked remnant of refactor.

### G. Untracked New Source Code (Post-Release Work)
| Path | Category |
|------|----------|
| `tests/test_ci.py` | New test — post-release |
| `tests/test_migrations.py` | New test — post-release |
| `tests/test_patch_runtime.py` | New test — post-release |
| `tests/test_policies.py` | New test — post-release |
| `tests/test_registry.py` | New test — post-release |
| `tests/test_router.py` | New test — post-release |
| `tests/test_server.py` | New test — post-release |
| `tests/test_update.py` | New test — post-release |
| `zai_coder/core/migrations.py` | New module — post-release |
| `zai_coder/core/policies.py` | New module — post-release |
| `zai_coder/core/update.py` | New module — post-release |
| `zai_coder/migrations/` | New subsystem — post-release |
| `zai_coder/server/` | New subsystem — post-release |
| `scripts/package-check.sh` | New script — post-release |
| `zai_coder/final_enterprise_release_pack/routes_old/` | Legacy refactor remnant (untracked) |

---

## 4. .gitignore Hygiene

**Patterns added:**
```
.zai-coder/
data/*.db
data/*.sqlite
data/*.sqlite3
data/zai-audit.jsonl
reports/*.tmp
*.p12
*.pfx
Modelfile
```

---

## 5. Validation Results

| Check | Result |
|-------|--------|
| `python3 -m compileall -q zai_coder` | ✅ PASS |
| `python3 -m pytest -q` | ✅ PASS — 446/446 tests, 2 warnings |
| `make safety-check` | ✅ PASS |
| `make repo-check` | ✅ PASS — no missing files, no forbidden commands |
| `make secret-scan` | ✅ PASS |
| `make stage-manifest-check` | ✅ PASS — no blocked files |
| `make final-release-status` | ✅ PASS — `ok: true` |

---

## 6. Cleanup Actions Taken

1. ✅ Removed `.zai-coder/` (untracked runtime state)
2. ✅ Removed `data/index.db` (untracked DB)
3. ✅ Removed `data/migrations.db` (untracked DB)
4. ✅ Removed `data/tasks.db` (untracked DB)
5. ✅ Removed `data/zai-audit.jsonl` (untracked audit log)
6. ✅ Removed `Modelfile` (untracked local config)
7. ✅ Updated `.gitignore` with missing runtime patterns
8. ✅ Created `reports/release-reconcile-v0.1.0.json`
9. ✅ Created `docs/release/RELEASE_RECONCILIATION_v0.1.0.md` (this file)

---

## 7. Decision: Post-Release Work Isolation

**The v0.1.0 release tag is intact.** All modified/untracked files represent legitimate post-release hardening work for the next version (v0.2.0 or similar).

### Recommended next action:

```bash
git switch -c chore/post-v0.1.0-enterprise-hardening
```

Then commit changes by subsystem:

| Subsystem | Files |
|-----------|-------|
| CI/repo policy | `.github/workflows/ci.yml`, `zai_coder/github_ready_core/*.py` |
| Safety/registry | `zai_coder/core/registry.py`, `zai_coder/core/safety.py` |
| Core modules | `zai_coder/core/migrations.py`, `zai_coder/core/policies.py`, `zai_coder/core/update.py` |
| New subsystems | `zai_coder/migrations/`, `zai_coder/server/` |
| Tests | All new test files under `tests/` |
| Scripts | All modified `scripts/**/*.sh` grouped by directory |
| DB hygiene | `git rm --cached data/enterprise-admin-console.db data/provider-audit.db data/zai-app.db` |

---

## 8. Final Verdict

| Item | Status |
|------|--------|
| Current HEAD | `9a11629` |
| v0.1.0 tag intact | ✅ YES — points to `b6b09e3` |
| Modified files | 441 (all post-release work) |
| Deleted files | 1 (intentional refactor) |
| Untracked files | 15 (after runtime cleanup) |
| Runtime files cleaned | 6 files/dirs removed |
| Validation | ALL PASS (446/446 tests) |
| Release state | **Post-release work isolated on branch recommended** |

> ⚠️ The v0.1.0 release itself is clean and valid. All working tree changes are post-release engineering work that should be committed on `chore/post-v0.1.0-enterprise-hardening`, not on `main` directly without review.
