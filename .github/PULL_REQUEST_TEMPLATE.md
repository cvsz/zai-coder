## Summary

Describe the change.

## Validation

- [ ] `python3 -m pytest -q`
- [ ] `make repo-check`
- [ ] `make secret-scan`
- [ ] `make stage-manifest-check`

## Safety

- [ ] No secrets
- [ ] No generated runtime artifacts
- [ ] No `apps/zlms/**`
- [ ] Exact-path staging only
