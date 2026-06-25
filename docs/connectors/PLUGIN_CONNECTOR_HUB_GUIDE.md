# Plugin Connector Hub Guide

## Commands

```bash
make plugin-connector-hub
make connector-status
make connector-catalog
make connector-search QUERY=cloud
make connector-validate CONNECTOR_ID=github
make connector-env-check CONNECTOR_ID=github
make connector-install-policy CONNECTOR_ID=github
make connector-install-demo APPLY=1
make connector-enable-demo APPLY=1
make connector-adapter-plans
make connector-sync-plan CONNECTOR_ID=github
make connector-webhook-draft CONNECTOR_ID=github
make connector-audit
make connector-export
make connector-dashboard-export
```

## Routes

```text
/api/connectors/status
/connectors
/connectors/catalog
/connectors/policy
/connectors/sync
```
