# Monitoring and Logging

## Logging

The production hardening core includes JSON log formatting.

## Recommended signals

- `/healthz`
- `/readyz`
- HTTP status counts
- session creation/revocation count
- migration status
- backup success/failure
- worker job failures
- integration approval events

## Log retention

Use logrotate or container logging driver. Keep sensitive data out of logs.
