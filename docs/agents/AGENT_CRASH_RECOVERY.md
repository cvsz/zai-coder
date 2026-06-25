# Agent Crash Recovery

Recovery steps:

1. mark agent crashed
2. capture heartbeat and task state
3. write audit event
4. check recovery budget
5. enqueue recovery worker job
6. restart only after lifecycle gate passes
