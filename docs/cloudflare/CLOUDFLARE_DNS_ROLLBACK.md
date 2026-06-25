# DNS Rollback Plan

If public verification fails:

1. Remove or disable DNS route.
2. Stop cloudflared service if needed.
3. Keep local origin running.
4. Review tunnel logs.
5. Review Access logs.
6. Verify localhost health.
7. Restore previous DNS only after root cause is known.
