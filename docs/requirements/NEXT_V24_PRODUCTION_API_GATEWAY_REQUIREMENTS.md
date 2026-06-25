# ZAI Coder Control Plane v24 — Production API Gateway Requirements

## Added in v24

- Gateway router.
- Request/response envelope.
- Tenant-aware auth guard.
- API-key/session guard.
- Rate-limit policy.
- CORS/security headers.
- Upstream service registry.
- OpenAPI gateway manifest.
- Gateway error handling.
- Gateway audit hooks.
- Gateway scripts/routes/docs/tests.

## Safety

- Localhost-first upstreams.
- Cloudflare Access expected before public exposure.
- Auth required by default.
- Tenant context required by default.
- Gateway audit redacts authorization/API-key headers.
- CORS defaults to localhost.
