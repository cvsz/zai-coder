# Cloudflare Tunnel Checklist

## Goal

Expose ZAI App Studio safely through Cloudflare only after local auth and API key checks are enabled.

## Preflight

- [ ] API auth enabled.
- [ ] Dashboard bound to localhost first.
- [ ] No secrets in repository.
- [ ] Cloudflare Access policy configured.
- [ ] Tunnel routes point to `http://127.0.0.1:8765`.
- [ ] Logs reviewed.
- [ ] Rollback plan prepared.

## Suggested hostname

```text
zai.zeaz.dev
```

## Safety

Do not expose `0.0.0.0:8765` publicly without Cloudflare Access or equivalent auth.
