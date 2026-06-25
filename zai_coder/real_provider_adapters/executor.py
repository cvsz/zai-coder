from __future__ import annotations
from .models import ProviderContext, ProviderOperation, ProviderResult
from .env_validation import validate_provider_env
from .permissions import permission_decision
from .approval_guard import approval_decision
from .audit import ProviderAuditLog

class ProviderExecutor:
    def __init__(self, audit_log: ProviderAuditLog | None = None):
        self.audit_log = audit_log or ProviderAuditLog()
    def execute(self, context: ProviderContext, operation: ProviderOperation) -> ProviderResult:
        blocked: list[str] = []
        env_report = validate_provider_env(operation.provider, context.env, apply=context.apply)
        if not env_report['ok']:
            blocked.extend(env_report.get('missing', []))
            blocked.extend(env_report.get('issues', []))
        perm = permission_decision(context.roles, context.scopes, context.apply)
        if not perm['allowed']:
            blocked.append(f"missing permission: {perm['permission']}")
        approval = approval_decision(context.apply, context.approval_id)
        if not approval['allowed']:
            blocked.append(approval['reason'])
        if blocked:
            result = ProviderResult(False, operation.provider, operation.action, not context.apply, 'provider operation blocked', operation.commands, blocked_reasons=tuple(blocked))
            event = self.audit_log.record(context, operation, result)
            return ProviderResult(result.ok, result.provider, result.action, result.dry_run, result.message, result.commands, event.id, result.blocked_reasons)
        if not context.apply:
            result = ProviderResult(True, operation.provider, operation.action, True, 'dry-run provider operation plan generated', operation.commands)
        else:
            result = ProviderResult(True, operation.provider, operation.action, False, 'apply permitted; execute commands manually or through approved runner', operation.commands)
        event = self.audit_log.record(context, operation, result)
        return ProviderResult(result.ok, result.provider, result.action, result.dry_run, result.message, result.commands, event.id, result.blocked_reasons)
