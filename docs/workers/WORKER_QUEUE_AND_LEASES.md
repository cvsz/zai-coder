# Worker Queue and Leases

Jobs move through:

```text
queued -> leased -> running -> completed
queued -> leased -> failed -> queued/dead_letter
```

Leases include worker id and expiry timestamp.
