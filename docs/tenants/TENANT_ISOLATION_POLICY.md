# Tenant Isolation Policy

Rules:

- Principal org must match target org.
- Workspace must match unless tenant admin/owner.
- Provider apply requires provider apply permission.
- Audit events are scoped by org/workspace.
- API keys are scoped by org/workspace.
