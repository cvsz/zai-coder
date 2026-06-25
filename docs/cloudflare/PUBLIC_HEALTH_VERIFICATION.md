# Public Health Verification

Expected checks:

```bash
curl -fsS http://127.0.0.1:8765/healthz
curl -fsS http://127.0.0.1:8765/readyz
curl -I https://zai.example.com/healthz
curl -I https://zai.example.com/api/status
```

Protected API should return an Access challenge or 401/403 without a valid session.
