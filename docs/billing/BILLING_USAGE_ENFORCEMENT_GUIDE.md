# Billing Usage Enforcement Guide

## Commands

```bash
make billing-usage-enforcement
make billing-status
make billing-plans
make plan-policy PLAN_ID=free
make usage-record-demo APPLY=1
make usage-summary
make quota-enforcement PLAN_ID=free
make overage-alerts PLAN_ID=free
make invoice-draft PLAN_ID=free
make invoice-write APPLY=1 PLAN_ID=free
make billing-audit
make billing-dashboard-export
```

## Routes

```text
/api/billing/status
/billing
/billing/plans
/billing/usage
/billing/invoice
```
