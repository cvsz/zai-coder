from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

@dataclass(frozen=True)
class ProviderContext:
    provider: str
    actor: str = 'local-operator'
    roles: tuple[str, ...] = ('admin',)
    scopes: tuple[str, ...] = ('providers:plan',)
    apply: bool = False
    approval_id: str = ''
    env: dict[str, str] = field(default_factory=dict)
    created_at: str = field(default_factory=now_iso)
    def to_safe_dict(self) -> dict:
        return {'provider': self.provider, 'actor': self.actor, 'roles': list(self.roles), 'scopes': list(self.scopes), 'apply': self.apply, 'approval_id': self.approval_id, 'env_keys': sorted(self.env.keys()), 'created_at': self.created_at}

@dataclass(frozen=True)
class ProviderOperation:
    provider: str
    action: str
    target: str
    commands: tuple[str, ...] = ()
    payload: dict[str, Any] = field(default_factory=dict)
    mutating: bool = False
    def to_dict(self) -> dict:
        return {'provider': self.provider, 'action': self.action, 'target': self.target, 'commands': list(self.commands), 'payload': dict(self.payload), 'mutating': self.mutating}

@dataclass(frozen=True)
class ProviderResult:
    ok: bool
    provider: str
    action: str
    dry_run: bool
    message: str
    commands: tuple[str, ...] = ()
    audit_id: str = ''
    blocked_reasons: tuple[str, ...] = ()
    def to_dict(self) -> dict:
        return {'ok': self.ok, 'provider': self.provider, 'action': self.action, 'dry_run': self.dry_run, 'message': self.message, 'commands': list(self.commands), 'audit_id': self.audit_id, 'blocked_reasons': list(self.blocked_reasons)}
