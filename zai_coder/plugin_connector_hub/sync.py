"""Connector sync planning."""

from __future__ import annotations

import uuid

from .models import ConnectorSyncPlan
from .catalog import find_connector


def connector_sync_plan(connector_id: str, org_id: str = "org_local", workspace_id: str = "ws_default", action: str = "status") -> ConnectorSyncPlan:
    connector = find_connector(connector_id)
    if action not in connector.supported_actions:
        raise ValueError(f"unsupported connector action: {action}")
    return ConnectorSyncPlan(
        id=f"sync_{uuid.uuid4().hex[:12]}",
        connector_id=connector_id,
        org_id=org_id,
        workspace_id=workspace_id,
        action=action,
        steps=(
            "validate connector manifest",
            "validate tenant connector permissions",
            "validate env without exposing secrets",
            f"prepare dry-run action: {action}",
            "record connector audit event",
        ),
    )


def sync_schedule_policy() -> dict:
    return {
        "dry_run": True,
        "default_interval_minutes": 60,
        "min_interval_minutes": 15,
        "tenant_scoped": True,
        "external_calls_disabled_by_default": True,
    }
