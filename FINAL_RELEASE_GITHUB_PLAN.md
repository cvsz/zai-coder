# Final Release GitHub Plan (Manual Only)

This release plan must be executed manually. **Do not run automated publishing commands.**

1. **Tag Release:** 
   Run: `make gpg-tag TAG_NAME="v50-final-enterprise-release"`

2. **Push Tag:**
   Run: `git push origin v50-final-enterprise-release` (manual-only, GPG-signed if supported)

3. **Release Assets:**
   Manually upload `zai-coder-clean-release.tgz` and `zai-coder-clean-release.sha256` to the GitHub Release page.

4. **Add Notes:**
   Paste content from `FINAL_RELEASE_NOTES.md` into the GitHub release description.

**WARNING:** Ensure no secret-bearing files are uploaded as CI artifacts or attached to the release.
