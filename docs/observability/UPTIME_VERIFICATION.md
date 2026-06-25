# Uptime Verification

```bash
make uptime-plan BASE_URL=http://127.0.0.1:8765 PUBLIC_URL=https://zai.example.com
```

Expected:

- local health returns 200
- local readiness returns 200
- public protected API returns Access challenge or 401/403
