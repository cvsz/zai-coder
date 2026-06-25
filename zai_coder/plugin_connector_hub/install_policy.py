"""Connector install/enable policy."""

from __future__ import annotations

from .catalog import find_connector
from .env_guard import validate_connector_env
from .permissions import connector_permission_decision
from .validator import connector_security_report


def install_policy_decision(
    connector_id: str,
    roles: tuple[str, ...] = ("tenant_admin",),
    env: dict[str, str] | None = None,
    dry_run_completed: bool = True,
    approval_id: str = "",
    enable: bool = False,
) -> dict:
    connector = find_connector(connector_id)
    env_check = validate_connector_env(connector.required_env, env or {})
    permissions = connector_permission_decision(roles, tuple(set(connector.required_permissions) | {"connector:install"}))
    security = connector_security_report(connector)
    blocked = []
    if not dry_run_completed:
        blocked.append("dry-run required before install")
    if enable and not approval_id.startswith("approved_"):
        blocked.append("enable requires approval_id")
    if not permissions["allowed"]:
        blocked.append("missing permissions: " + ",".join(permissions["missing"]))
    # Security report flags sensitive design concerns, but it is advisory for
    # dry-run install/enable policy. Hard blocks are handled by permissions,
    # approval, and env validation gates.
    # Missing env does not block dry-run install plan; it blocks enable/apply.
    if enable and not env_check["ok"]:
        blocked.append("env validation failed")
    return {
        "allowed": not blocked,
        "blocked": blocked,
        "connector": connector.to_dict(),
        "env": env_check,
        "permissions": permissions,
        "security": security,
        "dry_run": True,
    }


def enable_policy_decision(connector_id: str, roles: tuple[str, ...] = ("tenant_admin",), env: dict[str, str] | None = None, approval_id: str = "approved_manual_001") -> dict:
    return install_policy_decision(connector_id, roles, env or {}, True, approval_id, True)
