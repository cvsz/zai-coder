# Payment Provider Sandbox Guide

## Commands

```bash
make payment-provider-sandbox
make payment-status
make payment-env-check PROVIDER=sandbox
make checkout-draft ORG_ID=org_local PLAN_ID=free
make subscription-lifecycle
make webhook-draft ORG_ID=org_local
make plan-change-workflow CURRENT_PLAN_ID=free TARGET_PLAN_ID=pro
make failed-payment-policy PLAN_ID=pro
make billing-email-templates
make no-real-charge-gate
make payment-audit
make payment-dashboard-export
```

## Routes

```text
/api/payments/status
/payments
/payments/checkout
/payments/subscription
/payments/webhooks
```
