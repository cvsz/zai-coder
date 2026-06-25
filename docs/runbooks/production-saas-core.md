# Runbook — Production SaaS Core

## Preflight

```bash
python3 -m pytest -q
make production-saas-core
make saas-status-demo
```

## First-run plan

```bash
make first-run-plan ADMIN_EMAIL=admin@example.com
```

## Deployment plan

```bash
make saas-deployment-plan HOSTNAME=zai.zeaz.dev
```

## Migrations

```bash
make saas-migrations-plan
make saas-migrations-apply APPLY=1
```

## Worker

```bash
make worker-once
```

## Dashboards

```bash
make saas-dashboard-demo
```

## Safety

- Keep dashboard localhost-first until auth is fully enforced.
- Use API keys and role checks for production routes.
- Check quota before expensive actions.
- Audit every integration action.
