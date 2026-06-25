# Release Automation and Update Center Guide

## Commands

```bash
make release-automation-update-center
make release-center-status
make release-channels CHANNEL=stable
make version-plan CURRENT=v28.0.0 BUMP=minor CHANNEL=stable
make release-plan
make changelog-generate
make update-manifest APPLY=1
make update-plan
make rollback-migration-gate
make github-release-draft
make release-audit
make release-audit APPLY=1
make release-dashboard-export
```

## Routes

```text
/api/release-center/status
/release-center
/release-center/plan
/release-center/updates
/release-center/channels
```
