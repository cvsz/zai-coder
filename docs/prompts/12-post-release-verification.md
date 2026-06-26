# Prompt: Post-Release Verification

```text
You are working locally in:

/home/zeazdev/zai-coder

Phase:
Post-Release Verification — Verify Published Release and Record Evidence

Branch:
docs/v0.1.4-post-release-verification

Goal:
After v0.1.4 is published, verify the signed tag, GitHub release, assets, checksums, validation gates, and generated-file exclusion. Record the evidence in a post-release verification doc through a PR.

Critical rules:
- Do not rewrite tags.
- Do not republish release.
- Do not replace assets.
- Do not push directly to main.
- Do not commit dist artifacts.
- Stage exact verification doc only.

Steps:

cd /home/zeazdev/zai-coder

git fetch origin --prune --tags
git switch main
git pull --ff-only origin main
git status --short
git switch -c docs/v0.1.4-post-release-verification

Verify release:

git tag -v v0.1.4
git show --no-patch --decorate v0.1.4
gh release view v0.1.4 --repo cvsz/zai-coder --json tagName,name,isDraft,isPrerelease,url,assets,targetCommitish

Run validation:

python3 -m compileall -q zai_coder
python3 -m pytest -q
make repo-check
make secret-scan
make stage-manifest-check
./scripts/repo/check-generated-state.sh
./scripts/repo/check-ci-pytest-setup.sh
make package APPLY=1
make package-check
sha256sum -c dist/zai-coder-standalone-0.1.4.tar.gz.sha256
sha256sum -c dist/zai-coder-standalone-0.1.4.zip.sha256

Create:
- docs/release/V0.1.4_POST_RELEASE_VERIFICATION.md

Include:
- version
- main HEAD
- tag SHA
- tag verification
- GitHub release URL
- asset list
- checksum verification
- test result
- repo-check result
- secret-scan result
- stage-manifest-check result
- generated-state guard result
- CI pytest setup guard result
- package-check result
- generated-file exclusion result
- next phase recommendation

Generated-file exclusion:

git status --short
git ls-files dist .zai-coder .pytest_cache status.txt data/*.db data/**/*.db '*.sqlite' '*.sqlite3' 2>/dev/null || true

git add docs/release/V0.1.4_POST_RELEASE_VERIFICATION.md
git commit -S -m "docs: verify v0.1.4 release"
git push -u origin docs/v0.1.4-post-release-verification

gh pr create \
  --base main \
  --head docs/v0.1.4-post-release-verification \
  --draft \
  --title "docs: verify v0.1.4 release" \
  --body-file docs/release/V0.1.4_POST_RELEASE_VERIFICATION.md

Report:
1. branch
2. tag verification
3. GitHub release verification
4. asset list
5. checksum result
6. validation result
7. generated-file exclusion
8. verification commit hash
9. draft PR URL
10. final recommendation
```
