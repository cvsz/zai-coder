# Roadmap

Last updated: 2026-06-27

This is the canonical tracked roadmap for the ZAI Coder Control Plane. It separates verified release-ready work from remaining production hardening so the project does not claim shipped behavior that is still a dry-run scaffold or local-only plan.

## Current Release State

The repository is in a v50 final enterprise release-candidate state for local-first packaging and control-plane workflows.

Verified as release-ready:

- Source package gates: `compileall`, full `pytest`, `repo-check`, `secret-scan`, `stage-manifest-check`, `final-release-status`, source-package verification, checksum generation, and SBOM generation.
- Local-first execution model: dry-run-first command routing, provider-operation planning, safety checks, and approval-gated apply paths.
- Release/security guardrails: tracked-source secret scanning, exact-path stage manifest validation, forbidden-command checks, and local-only release artifact generation.
- Enterprise modules: governance, compliance center, SSO identity, reporting board pack, observability, execution runner, provider adapters, tenant controls, connector hub, disaster recovery, go-live command center, and final release pack foundations.

Recently hardened:

- Release secret scan now scans tracked source files in git checkouts and ignores untracked vendor/import drops.
- QA command execution preserves quoted arguments with shell-safe parsing.
- Route payloads now parse form-style booleans such as `"false"` safely across apply/governance surfaces.
- Backup restore now rejects archive traversal, blocked app paths, links, and special tar members before extraction.
- Compliance evidence ingestion now rejects absolute paths, parent traversal, secret-bearing paths, and credential paths.

## Open Production Gaps

These are the remaining gaps before claiming external, always-on production service readiness.

| Area | Gap | Production risk | Target |
| --- | --- | --- | --- |
| Runtime server | FastAPI/ASGI runtime is optional and reports missing production dependencies unless `requirements-production.txt` is installed. | Deployments can pass local package tests but fail to serve if production extras are absent. | v51 |
| Production API gateway | Gateway modules are primarily route/planning surfaces, not a fully managed live reverse proxy with TLS and upstream health failover. | Public exposure would need external gateway hardening. | v51 |
| Auth/session operations | Local auth/session foundations exist, but enterprise SSO/session lifecycle needs end-to-end runtime validation against real deployment config. | Misconfigured auth can allow weak deployment posture. | v51 |
| Persistence | Several dashboards and reports use static/local snapshots; not all metrics, evidence, audit, and KPI streams have durable retention policies. | Restart or local file cleanup can lose operational history. | v52 |
| Observability | Health checks and trend reports exist, but alert deduplication, saturation control, and SLO dashboards remain limited. | Noisy or missing alerts during incident response. | v52 |
| External providers | Provider adapters remain dry-run-first and require manual execution or an approved runner. | Correct for safety, but not full automated provider lifecycle management. | v52 |
| Frontend integration | `web/open-webui/` is currently an untracked working-tree import, not a tracked/release-gated product surface. | Release gates intentionally ignore it until ownership and packaging are decided. | Decision required |
| Versioning | Python package metadata and v50 release labels are not a simple semver line. | Downstream automation may need explicit version mapping. | v51 |

## Release Priorities

### v51: Production Runtime Gate

- Add a production-runtime validation target that installs or verifies `requirements-production.txt`, imports the ASGI server, and runs health/readiness probes.
- Promote the optional FastAPI dependency state into an explicit release report field.
- Add route-level tests for auth/session, gateway envelope handling, and provider apply-denial behavior with string and JSON payloads.
- Update package/version metadata strategy so v50-style release labels and Python package versions are mapped intentionally.

### v52: Durable Operations

- Add durable SQLite-backed stores for KPI snapshots, health trend history, compliance evidence inventory, and execution/provider audit streams where currently in-memory or file-only.
- Add backup restore integration tests for safe extraction into a temporary tree and rejected archive member types.
- Add observability alert deduplication, rate limits, and incident-review queues.
- Add an explicit retention policy for generated release, audit, and evidence artifacts.

### v53: External Deployment Readiness

- Add a production gateway deployment profile with TLS termination assumptions, upstream health failover, request-size limits, rate limits, and structured audit logging.
- Add documented Cloudflare Access and DNS preflight gates for public exposure.
- Add container/runtime smoke tests for the production Docker Compose profile.
- Keep publishing, pushing, and third-party mutations manual until an approved external-action workflow is implemented.

### v54: Frontend/Product Surface Decision

- Decide whether `web/open-webui/` is vendor reference, forked product code, or a tracked first-party UI.
- If first-party, add dependency install, lint, test, build, SBOM, license, and secret-scan gates for that tree.
- If vendor/reference only, move it outside the release tree or document it as an excluded local import.

## Done Criteria For Production-Ready Claims

A release can be called production-ready only when all of the following are true:

- `python3 -m compileall -q zai_coder` passes.
- `python3 -m pytest -q` passes.
- `make repo-check`, `make secret-scan`, `make stage-manifest-check`, and `make final-release-status APPLY=1` pass.
- `make verify-source-package`, `make release-checksums`, and `make release-sbom` pass.
- Production runtime import and health/readiness probes pass with production dependencies installed.
- No untracked product surface is required for the release.
- External mutation workflows remain manual-only unless a scoped approval and audit path exists.
- Release notes list known warnings and clearly distinguish shipped features from dry-run plans.

## Operating Rules

- Keep local-first and dry-run-first behavior as the default.
- Never hardcode secrets or include `.env` files in release artifacts.
- Keep release scans focused on tracked source files; scan imported vendor/product trees only after ownership is explicit.
- Treat public exposure as blocked until Cloudflare Access, auth, rate limiting, and rollback plans are verified.
- Keep roadmap items evidence-backed by tests, release gates, or generated reports.
