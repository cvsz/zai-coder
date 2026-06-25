# Tenant Migration Plan

Migration steps:

1. freeze mutating provider operations
2. create source tenant backup
3. verify source export integrity
4. create target tenant organization
5. import workspaces
6. re-issue tenant-scoped API keys
7. verify tenant isolation
8. run health and governance gates
9. unfreeze operations after approval
