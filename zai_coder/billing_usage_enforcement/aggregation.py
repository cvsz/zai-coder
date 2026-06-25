"""Workspace usage aggregation."""

from __future__ import annotations

from collections import defaultdict

from .models import WorkspaceUsageSummary


EVENT_TO_FIELD = {
    "run": "monthly_runs",
    "storage_mb": "storage_mb",
    "provider_apply": "provider_apply",
    "seat": "seats",
    "api_call": "api_calls",
}


def aggregate_workspace_usage(events: list[dict], org_id: str, workspace_id: str) -> WorkspaceUsageSummary:
    totals = defaultdict(int)
    for event in events:
        if event.get("org_id") != org_id or event.get("workspace_id") != workspace_id:
            continue
        field = EVENT_TO_FIELD.get(event.get("event_type"))
        if field:
            totals[field] += int(event.get("quantity", 0))
    return WorkspaceUsageSummary(
        org_id=org_id,
        workspace_id=workspace_id,
        monthly_runs=totals["monthly_runs"],
        storage_mb=totals["storage_mb"],
        provider_apply=totals["provider_apply"],
        seats=totals["seats"],
        api_calls=totals["api_calls"],
    )


def aggregate_org_usage(events: list[dict], org_id: str) -> dict:
    summaries: dict[str, WorkspaceUsageSummary] = {}
    workspaces = sorted({event.get("workspace_id") for event in events if event.get("org_id") == org_id})
    for workspace_id in workspaces:
        if workspace_id:
            summaries[workspace_id] = aggregate_workspace_usage(events, org_id, workspace_id)
    return {"org_id": org_id, "workspaces": {key: value.to_dict() for key, value in summaries.items()}}
