from __future__ import annotations
ROLE_PERMISSIONS = {'owner': {'providers:*'}, 'admin': {'providers:plan', 'providers:apply', 'providers:audit'}, 'operator': {'providers:plan', 'providers:apply'}, 'viewer': {'providers:plan'}}

def permissions_for_roles(roles: tuple[str, ...]) -> set[str]:
    perms: set[str] = set()
    for role in roles:
        perms.update(ROLE_PERMISSIONS.get(role, set()))
    return perms

def has_provider_permission(roles: tuple[str, ...], scopes: tuple[str, ...], permission: str) -> bool:
    perms = permissions_for_roles(roles) | set(scopes)
    if 'providers:*' in perms or permission in perms:
        return True
    prefix = permission.split(':', 1)[0]
    return f'{prefix}:*' in perms

def permission_decision(roles: tuple[str, ...], scopes: tuple[str, ...], apply: bool) -> dict:
    permission = 'providers:apply' if apply else 'providers:plan'
    return {'allowed': has_provider_permission(roles, scopes, permission), 'permission': permission, 'roles': list(roles), 'scopes': list(scopes)}
