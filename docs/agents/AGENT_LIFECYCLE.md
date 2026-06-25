# Agent Lifecycle

Supported statuses:

```text
stopped -> starting -> running
running -> paused
running -> draining -> stopped
running -> crashed -> starting
any safe end -> terminated
```
